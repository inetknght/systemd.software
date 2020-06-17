#!/usr/bin/env python3

import tornado.ioloop
import tornado.web
import tornado.template
import tornado.escape

from tornado.options import options
from tornado.options import parse_command_line
from tornado.options import define as define_opt

from lib.tornado_uds_app import Application

define_opt("listen-path", type=str, help="Path to the socket for nginx to talk to me", default=None)
define_opt("listen-port", type=str, help="Port number for TCP listen for nginx to talk to me", default=None)

class Redirector(tornado.web.RequestHandler):
    REDIRECT_TARGET = 'https://github.com/inetknght/systemd.software'
    REDIRECT_LEARN_MORE = '<p>Learn more at <a href="https://systemd.software/index.html">https://systemd.software/index.html</a></p>'
    def get(self):
        shown = self.get_argument('shown', default='0')
        if None != shown and '1' == shown:
            self.set_status(301) # permanent redirect
            self.add_header("Location", self.REDIRECT_TARGET)
            self.finish()
            return
        self.set_status(200)
        self.render(
            template_name = "redirect.html",
            here = self.request.path,
            target = self.REDIRECT_TARGET,
            more = self.REDIRECT_LEARN_MORE,
        )

class NetworkManagerCLI(Redirector):
    # `nmcli` isn't actually a systemd service.
    # It's provided by NetworkManager and is (unfortunately) part of GNOME.
    # However, it's commonly used on `systemd` systems and I frequently forget
    # that it's separate from systemd.
    #
    # TODO: describe this in a page with a link to the GNOME site.
    # (use REDIRECT_LEARN_MORE ... )
    REDIRECT_TARGET = 'https://developer.gnome.org/NetworkManager/stable/nmcli.html'

class RedirectorWithBase(Redirector):
    REDIRECT_BASE = 'https://systemd.software/'
    REDIRECT_TARGET = "index.html"
    def initialize(self):
        self.REDIRECT_TARGET = "{}{}".format(self.REDIRECT_BASE, self.REDIRECT_TARGET)

class SystemDManual(RedirectorWithBase):
    REDIRECT_BASE = 'https://www.freedesktop.org/software/systemd/man/'

class SystemDSoftwareRoot(SystemDManual):
    pass

class _Environment(SystemDManual):
    REDIRECT_TARGET = "environment.d"
class _FileHierarchy(SystemDManual):
    REDIRECT_TARGET = "file-hierarchy"
class _Positive(SystemDManual):
    REDIRECT_TARGET = "systemd.positive"

class RedirectorByName(Redirector):
    REDIRECT_BASE = "" # eg SystemDSoftware
    REDIRECT_TARGET = "https://www.freedesktop.org/software/systemd/man/"
    def initialize(self):
        # self.__class__.__name__ is the instantiated class name
        name = self.__class__.__name__.replace(self.REDIRECT_BASE, "")
        self.REDIRECT_TARGET = '{}{}'.format(self.REDIRECT_TARGET, name)

class RedirectorByNameLowercase(RedirectorByName):
    def initialize(self):
        super().initialize()
        self.REDIRECT_TARGET = self.REDIRECT_TARGET.lower()
rbnl = RedirectorByNameLowercase

class SystemDRedirectByName(rbnl):
    REDIRECT_BASE = "_"
    REDIRECT_TARGET = "https://www.freedesktop.org/software/systemd/man/systemd."
sdrbn = SystemDRedirectByName
class _Directives(sdrbn):
    pass
class _Service(sdrbn):
    pass
class _Timer(sdrbn):
    pass
class _Unit(sdrbn):
    pass
class _Socket(sdrbn):
    pass
class _Nspawn(sdrbn):
    pass
class _Mount(sdrbn):
    pass
class _AutoMount(sdrbn):
    pass
class _Path(sdrbn):
    pass
class _Link(sdrbn):
    pass

class Reboot(rbnl):
    pass
class Daemon(rbnl):
    pass
class JournalCtl(rbnl):
    pass
class SystemCtl(rbnl):
    pass
class MachineCtl(rbnl):
    pass
class NetworkCtl(rbnl):
    pass

def make_app():
    return Application([
        # Root
        (r"/", SystemDSoftwareRoot),
        #
        # Manual pages, non-commands
        (r"/env(?:ironment)?s?", _Environment),
        (r"/(?:hier|file(?:s|-hierarch(?:y|ies)?)|filesystem|director(?:y|ies)?)", _FileHierarchy),
        (r"/daemon", Daemon),
        (r"/(?:positive|dnssec)", _Positive),
        #
        # Manuals for unit files
        (r"/directives?", _Directives),
        (r"/services?", _Service),
        (r"/timers?", _Timer),
        (r"/units?", _Unit),
        (r"/sockets?", _Socket),
        (r"/mounts?", _Mount),
        (r"/automounts?", _AutoMount),
        (r"/paths?", _Path),
        (r"/links?", _Link), # see also networkctl
        #
        # Manuals for commands
        (r"/(?:n?spawn|container)s?", _Nspawn),
        (r"/(?:halt|re-?boot|power-?off|shut-?down)", Reboot),
        (r"/(?:journal(?:cn?tl|control)?|logs?)", JournalCtl),
        (r"/(?:system(?:cn?tl|control)?)", SystemCtl),
        (r"/(?:machine(?:cn?tl|control)?)", MachineCtl),
        (r"/(?:network(?:cn?tl|control)?)", NetworkCtl), # See also systemd.link
        #
        # Misnomers
        (r"/nmcli", NetworkManagerCLI)
    ],
        template_path = "templates"
    )

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    if None != options.listen_path:
        app.listen(uds_path = options.listen_path)
    else:
        if None != options.listen_port:
            app.listen(port = options.listen_port)
        else:
            raise RuntimeError("use --listen-path or --listen-port")
    tornado.ioloop.IOLoop.current().start()
