# coding: utf-8
#!/usr/bin/env python
'''
Processo responsavel por consumir a fila do beanstalkd, e expirar o cache nos nginxs
'''

import os, sys, getopt, logging

def usage():
    print "\MSS Beanstalk daemon consummer:"
    print "usage: friends_finder.py [--env=ENV_RUN][--tube=context][--help] COMMAND"
    print "\nOs comandos podem ser:"
    print "     start       incia o consumidor"
    print "     stop        para o consumidor"
    print "     restart     reinicia"
    print "     help        mostra esse help\n"
    
def main():

    try:
        optlists, command = getopt.getopt(sys.argv[1:], "het", ["help", "env="])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    env = "LOCAL"
    
    for opt, value in optlists:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-e", "--env"):
            env = value
    
    pidfile = "/opt/logs/mss/friendsfinder.pid"
    
    if not command or command[0] not in ["start","stop","restart"]:
        usage()
        sys.exit()

    project_root = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, os.path.abspath("%s/.." % project_root))
    
    logging.basicConfig(
        level = logging.DEBUG,
        format = '%(asctime)s %(levelname)s %(message)s',
        filename = "/opt/logs/mss/friendsfinder.log",
        filemode = 'a'
    )

    # settings
    from mss import core
    if env == "LOCAL":
        from mss import settings_local as settings
    else:
        from mss import settings
    
    core.settings = settings

    from mss.core.finder import FriendsFinder
    finder = FriendsFinder(pidfile=pidfile)

    if command[0] == "start":
        finder.run()

    elif command[0] == "stop":
        finder.stop()

    elif command[0] == "restart":
        finder.restart()
    
if __name__ == "__main__":
    main()
