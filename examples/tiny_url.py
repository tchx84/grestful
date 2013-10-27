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

import sys

from gi.repository import GObject

sys.path.append("..")
from grestful.object import Object
from grestful.decorators import asynchronous
from grestful.decorators import check_is_not_created


class TinyUrl(Object):

    CREATE_URL = 'http://tiny-url.info/api/v1/create'

    @asynchronous
    @check_is_not_created
    def create(self, url):
        self._post(self.CREATE_URL, self._params(url))

    def _params(self, url):
        params = [
            ('apikey', 'INSERT_YOURS'),
            ('provider', '0_mk'),
            ('format', 'json'),
            ('url', url)]
        return params


def _completed_cb(tiny, result, loop):
    if result['state'] == 'ok':
        print 'TinyUrl is %s' % result['shorturl']
    loop.quit()


def _failed_cb(tiny, exception, loop):
    print 'Something went wrong!'
    loop.quit()

if __name__ == '__main__':
    loop = GObject.MainLoop()

    tiny = TinyUrl()
    tiny.connect('completed', _completed_cb, loop)
    tiny.connect('failed', _failed_cb, loop)
    tiny.create('http://github.com/tchx84/grestful')

    loop.run()
