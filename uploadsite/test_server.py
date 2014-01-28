#!/usr/bin/env python

import os
import CGIHTTPServer

class PyCGIHandler(CGIHTTPServer.CGIHTTPRequestHandler):
    def is_cgi(self):
        splitpath = CGIHTTPServer._url_collapse_path_split(self.path)
        script_query = splitpath[1].split("?", 1)
        if script_query[0].endswith(".py"):
            if splitpath[0].startswith("/"):
                # Workaround for some weirdness with how CGIHTTPServer
                # computes the SCRIPT_NAME environment variable.
                splitpath = list(splitpath)
                splitpath[0] = ''
                splitpath = tuple(splitpath)
            self.cgi_info = splitpath
            return True
        return False

os.chdir("www")
CGIHTTPServer.test(HandlerClass=PyCGIHandler)
