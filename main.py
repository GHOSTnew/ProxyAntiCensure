##################################################################################
#                       Copyright (C) 2014, GHOSTnew                             #
##################################################################################
# The MIT License (MIT)                                                          #
#                                                                                #
# Permission is hereby granted, free of charge, to any person obtaining a copy   #
# of this software and associated documentation files (the "Software"), to deal  #
# in the Software without restriction, including without limitation the rights   #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      #
# copies of the Software, and to permit persons to whom the Software is          #
# furnished to do so, subject to the following conditions:                       #
#                                                                                #
# The above copyright notice and this permission notice shall be included in     #
# all copies or substantial portions of the Software.                            #
#                                                                                #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN      #
# THE SOFTWARE.                                                                  #
##################################################################################


from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.web.client import downloadPage

import base64
import os


class Configuration:

    URL = None

    def __init__(self):
        self.URL = "http://site.com"


class MyProxy(Resource):
    isLeaf = True

    def __init__(self, conf):
        self.config = conf

    def render_GET(self, request):
        if ".css" in request.uri:
            request.setHeader("Content-Type", "text/css")
        print(request.uri)
        page = self.getPage(request.uri)
        if page is not None:
            return page
        else:
            request.setResponseCode(404)
            self.dlPage(request.uri)
            return """<html>
    <head>
        <title> 404 not found</title>
        <meta http-equiv="refresh" content="10" >
    </head>
    <body>
        <h1>%s not found</h1>
        <p>Nous allons tenter de telecharger la page</p>
    </body>
</html>""" % (request.uri,)

    def dlPage(self, uri):
        print("telechargement de " + uri)
        downloadPage(self.config.URL + uri, "site/" + base64.b64encode(uri)).addCallback(self.dlHandler)

    def dlHandler(self, result):
        print("telechargement finis")
        print(result)

    def getPage(self, uri):
        path = "site/" + base64.b64encode(uri)
        if os.path.exists(path):
            page = ""
            with open(path, "r") as p:
                page = p.read()
            return page
        else:
            return None

if __name__ == "__main__":
    if os.path.exists("site") is False:
        os.mkdir("site")
    resource = MyProxy(Configuration())
    factory = Site(resource)
    reactor.listenTCP(8080, factory)
    reactor.run()
