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

from gi.repository import GObject

from .errors import AlreadyCreatedError
from .errors import NotCreatedError


def check_is_created(method):
    """ Make sure the Object DOES have an id, already. """
    def check(self, *args, **kwargs):
        if self.id is None:
            raise NotCreatedError('%s does not exists.' %
                                  self.__class__.__name__)
        return method(self, *args, **kwargs)
    return check


def check_is_not_created(method):
    """ Make sure the Object does NOT have an id, yet. """
    def check(self, *args, **kwargs):
        if self.id is not None:
            raise AlreadyCreatedError('%s.id %s already exists.' %
                                     (self.__class__.__name__, self.id))
        return method(self, *args, **kwargs)
    return check


def asynchronous(method):
    """ Convenience wrapper for GObject.idle_add. """
    def _async(*args, **kwargs):
        GObject.idle_add(method, *args, **kwargs)
    return _async
