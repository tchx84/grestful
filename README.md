## gRESTful
gRESTful helps you integrate RESTful web services with your Glib2 code.

### Example
This is a quick example for the TinyUrl RESTful API. Yes, that is all you
need. Check the examples directory for the full example.

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

For a more complex example check https://github.com/tchx84/journalx-gobject.

### Dependencies
* python 2.7.x
* pygobject3
* pycurl

### Features
* Asynchronous to the bone.
* Access RESTful resources just as if they were GObject-based objects.
* Extremely easy to use.

### Development
* Feel free to hack it and send pull requests ;)
