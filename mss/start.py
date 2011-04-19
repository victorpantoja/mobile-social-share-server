# coding: utf-8
#!/usr/bin/env python

import os, sys
import tornado.options
import logging
    
def main():
    project_root = os.path.abspath(os.path.dirname(__file__))
    
    tornado.options.define("port", type=int, default=9080, help="port to listen")
    tornado.options.define("conf", default="settings.py", help="config file")
    tornado.options.define("pidfile", type=str, default="/opt/logs/mss/mss.pid", help="pidfile")
    tornado.options.define("as_daemon", type=bool, default=False, help="run server as daemon")
    tornado.options.define("template_dir", type=str, default="%s/templates" % project_root)
    tornado.options.define("media_dir", type=str, default="%s/media" % project_root)
    tornado.options.define("EMAIL", type=dict)
    tornado.options.define("DATABASE_ENGINE", type=dict)
    tornado.options.define("DATABASE_POOL_SIZE", type=int)

    tornado.options.parse_command_line()        
    
    # settings, path.insert
    sys.path.insert(0, os.path.abspath("%s/.." % project_root))
    
    tornado.options.parse_config_file(project_root +"/"+ tornado.options.options.conf)
        
    logging.getLogger().setLevel(getattr(logging, tornado.options.options.logging.upper())) 
    
    # settings    
    from mss import core

    from mss import settings
    core.settings = settings
    
    from mss.core.server import MSSServer
    server = MSSServer()
    
    if tornado.options.options.as_daemon:
        
        commands = ["start", "stop", "restart"]
        command = ""
        for cmd in commands:
            if cmd in sys.argv[1:]:
                command = cmd
                
        if not command:
            tornado.options.print_help()
            print "As Daemon mode require command, start|stop|restart\n\n"
            sys.exit()

        if command == "start":
            server.start()

        elif command == "stop":
            server.stop()

        elif command == "restart":
            server.restart()
    else:
        server.run()
        
if __name__ == "__main__":
    main()