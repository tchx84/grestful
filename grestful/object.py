# Copyright (c) 2013 Martin Abente Lahaye. - martin.abente.lahaye@gmail.com
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.

import json
import pycurl
import urllib
import logging

from gi.repository import GObject

from .errors import TransferError
from .errors import ResponseError
from .errors import NotSupportedError


class Object(GObject.GObject):

    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'

    __gsignals__ = {
        'started':   (GObject.SignalFlags.RUN_FIRST, None,
                     ([])),
        'updated':   (GObject.SignalFlags.RUN_FIRST, None,
                     ([float, float, float, float])),
        'completed': (GObject.SignalFlags.RUN_FIRST, None,
                     ([object])),
        'failed':    (GObject.SignalFlags.RUN_FIRST, None,
                     ([object]))}

    def __init__(self, id=None):
        """ RESTful objects must have an id. """
        GObject.GObject.__init__(self)
        self.id = id

    def _get(self, url, params=None):
        """ Wrapper method for GET calls. """
        self._call(self.GET, url, params, None)

    def _post(self, url, params, uploads=None):
        """ Wrapper method for POST calls. """
        self._call(self.POST, url, params, uploads)

    def _delete(self, url):
        """ Wrapper method for DELETE calls. """
        self._call(self.DELETE, url, None, None)

    def _call(self, method, url, params, uploads):
        """ Initiate resquest to server and handle outcomes. """
        try:
            data = self._request(method, url, params, uploads)
        except Exception, e:
            self._failed_cb(e)
        else:
            self._completed_cb(data)

    def _request(self, method, url, params=None, uploads=None):
        """ Request to server and handle transfer status. """
        c = pycurl.Curl()

        if method == self.POST:
            c.setopt(c.POST, 1)
            if uploads is not None:
                if isinstance(uploads, dict):
                    # handle single upload
                    uploads = [uploads]
                for upload in uploads:
                    params += [(upload['field'],
                               (c.FORM_FILE, upload['path']))]

                c.setopt(c.HTTPPOST, params)
            else:
                # XXX memory leak in pyCurl/7.29.0?
                data = urllib.urlencode(params)
                c.setopt(c.POSTFIELDS, data)

        elif method == self.GET:
            c.setopt(c.HTTPGET, 1)
            if params:
                url += '?%s' % urllib.urlencode(params)

        elif method == self.DELETE:
            c.setopt(pycurl.CUSTOMREQUEST, self.DELETE)

        else:
            raise NotSupportedError(str(method))

        buffer = []

        def _write_cb(data):
            buffer.append(data)

        c.setopt(c.HTTPHEADER, self._hook_header(params))
        c.setopt(pycurl.SSL_VERIFYPEER, 0)
        c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(c.URL, url)
        c.setopt(c.NOPROGRESS, 0)
        c.setopt(c.PROGRESSFUNCTION, self._updated_cb)
        c.setopt(c.WRITEFUNCTION, _write_cb)
        c.setopt(c.FOLLOWLOCATION, 1)
        #c.setopt(c.VERBOSE, True)

        try:
            self.emit('started')
            c.perform()
        except pycurl.error, e:
            raise TransferError(str(e))
        else:
            code = c.getinfo(c.HTTP_CODE)
            if not 200 <= code < 300:
                raise ResponseError(code)
        finally:
            c.close()

        return ''.join(buffer)

    def _completed_cb(self, data):
        """ Extract info from data and emit completed. """
        try:
            info = json.loads(data)
        except ValueError:
            info = self._hook_data(data)
        except Exception, e:
            info = None
            logging.error('%s: _completed_cb crashed with %s',
                          self.__class__.__name__, str(e))
        finally:
            self._hook_id(info)
            self.emit('completed', info)

    def _failed_cb(self, exception):
        """ Emit failed signal, including the exception. """
        self.emit('failed', exception)

    def _updated_cb(self, downtotal, downdone, uptotal, updone):
        """ Emit update signal, including transfer status metadata. """
        self.emit('updated', downtotal, downdone, uptotal, updone)

    def _hook_id(self, info):
        """ Extract id from info. Override for custom behaviour. """
        if isinstance(info, dict) and 'id' in info.keys():
            self.id = info['id']

    def _hook_data(self, data):
        """ Transform data to info. Override for custom behaviour. """
        return data

    def _hook_header(self, params=None):
        """ Add custom headers. Override for custom behaviour. """
        return []
