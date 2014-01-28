#!/usr/bin/env python

import os
import CGIHTTPServer

class PyCGIHandler(CGIHTTPServer.CGIHTTPRequestHandler):
    def is_cgi(self):
        splitpath = CGIHTTPServer._url_collapse_path_split(self.path)
        script_query = splitpath[1].split("?", 1)
        if script_query[0].endswith(".py"):
            self.cgi_info = splitpath
            return True
        return False

os.chdir("www")
CGIHTTPServer.test(HandlerClass=PyCGIHandler)
