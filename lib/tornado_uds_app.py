
import os
import stat

import tornado.web
import tornado.httpserver
import tornado.netutil

class Application(tornado.web.Application):
    def listen(self, uds_path = None, port = None, *args, **kwargs):
        if None == uds_path:
            return super().listen(port, *args, **kwargs)
        if (0 != len(args)) or ('address' in kwargs) or ('port' in kwargs):
            # These are mutually exclusive arguments.
            raise ValueError("uds_path and network address or port specified")
        s = tornado.netutil.bind_unix_socket(uds_path)
        from tornado.httpserver import HTTPServer
        server = HTTPServer(self)
        server.add_socket(s)
