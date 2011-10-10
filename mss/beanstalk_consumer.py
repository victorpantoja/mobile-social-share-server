# coding: utf-8
#!/usr/bin/env python
'''
Processo responsavel por consumir a fila do beanstalkd, e expirar o cache nos nginxs
'''

import os, sys, getopt, logging

def usage():
    print "\MSS Beanstalk daemon consummer:"
    print "usage: beanstalk_consumer.py [--env=ENV_RUN][--tube=context][--help] COMMAND"
    print "\nOs comandos podem ser:"
    print "     start       incia o consumidor"
    print "     stop        para o consumidor"
    print "     restart     reinicia"
    print "     help        mostra esse help\n"
    
def main():

    try:
        optlists, command = getopt.getopt(sys.argv[1:], "het", ["help", "env=", "tube="])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    env = "PROD"
    tube = "context"
    
    for opt, value in optlists:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-e", "--env"):
            env = value
        elif opt in ("-t", "--tube"):
            tube = value
    
    pidfile = "/opt/logs/mss/beanstalkd-%s.pid" % tube
    
    if not command or command[0] not in ["start","stop","restart"]:
        usage()
        sys.exit()

    project_root = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, os.path.abspath("%s/.." % project_root))
    
    logging.basicConfig(
        level = logging.DEBUG,
        format = '%(asctime)s %(levelname)s %(message)s',
        filename = "/opt/logs/mss/beanstalkd.log",
        filemode = 'a'
    )

    # settings
    from mss import core
    from mss import settings
    
    core.settings = settings

    from mss.core.beanstalk import MSSBeanstalk
    mssBeanstalk = MSSBeanstalk(pidfile=pidfile, host=settings.BEANSTALK, tube=tube)

    if command[0] == "start":
        mssBeanstalk.start()

    elif command[0] == "stop":
        mssBeanstalk.stop()

    elif command[0] == "restart":
        mssBeanstalk.restart()
    
if __name__ == "__main__":
    main()
