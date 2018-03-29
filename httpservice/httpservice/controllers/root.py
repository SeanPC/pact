from pecan import expose,redirect,response
from webob.exc import status_map
from router import router
import json


class RootController(object):
    @expose(generic=True, template='json')
    def index(self):
        return dict()

    @index.when(method='PUT')
    def index_put(self,**data):
        print data
        data["method"] = "put"
        return router(data)

    @index.when(method='DELETE')
    def index_delete(self,**data):
        data["method"] = "delete"
        return router(data)

    @index.when(method='GET')
    def index_get(self,**data):
        data["method"] = "get"
        return router(data)

    @index.when(method='POST')
    def index_post(self,**data):
        data["method"] = "post"
        return router(data)
