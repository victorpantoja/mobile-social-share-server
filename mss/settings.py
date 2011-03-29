# coding: utf-8
#!/usr/bin/env python

log_file_prefix = "/opt/logs/monitor/monitor.log"
logging='debug'

EMAIL = {
    "server":"smtpar.globoi.com",
    "port":25,
}

DATABASE_ENGINE = {
    "read":"mysql://root@localhost/monitor?charset=utf8&use_unicode=0",
    "write":"mysql://root@localhost/monitor?charset=utf8&use_unicode=0"
}

DATABASE_POOL_SIZE = 25

hosts = {'globoesporte':
            {'dev01':{'hostname':'riovld168.globoi.com','username':'watcher','pass':'watch654','cmd':'cat /mnt/projetos/deploy-be/globoesporte01/app/current/version.txt'},
            'qa01':{'hostname':'riovld170.globoi.com','username':'watcher','pass':'watch654','cmd':'cat /mnt/projetos/deploy-be/globoesporte01/app/current/version.txt'},
            'staging':{'hostname':'riovlb13.globoi.com','username':'watcher','pass':'watch654','cmd':'cat /mnt/projetos/deploy-be/globoesporte/app/current/version.txt'},
            u'produção':{'hostname':'riolb176.globoi.com','username':'watcher','pass':'b2-4ac','cmd':'cat /mnt/projetos/deploy-be/globoesporte/app/current/version.txt'}
            },
        'globocore':
            {'dev01':{'hostname':'riovld168.globoi.com','username':'watcher','pass':'watch654','cmd':'cat /mnt/projetos/deploy-be/globoesporte01/app/current/globocore/version.txt'},
            'qa01':{'hostname':'riovld170.globoi.com','username':'watcher','pass':'watch654','cmd':'cat /mnt/projetos/deploy-be/globoesporte01/app/current/globocore/version.txt'},
            'staging':{'hostname':'riovlb13.globoi.com','username':'watcher','pass':'watch654','cmd':'cat /mnt/projetos/deploy-be/globoesporte/app/current/globocore/version.txt'},
            u'produção':{'hostname':'riolb176.globoi.com','username':'watcher','pass':'b2-4ac','cmd':'cat /mnt/projetos/deploy-be/globoesporte/app/current/globocore/version.txt'}
            },
        'dynamo-ge':
            {'dev01':{'hostname':'riovld121.globoi.com','username':'dynamo','pass':'dynamo','cmd':'cat /mnt/projetos/deploy-be/dynamo01/app/globoesporte/current/dynamogloboesporte/version.txt'},
            'qa01':{'hostname':'riovld122.globoi.com','username':'dynamo','pass':'dynamo','cmd':'cat /mnt/projetos/deploy-be/dynamo01/app/globoesporte/current/dynamogloboesporte/version.txt'},
            'staging':{'hostname':'riovlb13.globoi.com','username':'watcher','pass':'watch654','cmd':'cat /mnt/projetos/deploy-be/dynamo/app/globoesporte/current/dynamogloboesporte/version.txt'},
            u'produção':{'hostname':'riolb176.globoi.com','username':'watcher','pass':'b2-4ac','cmd':'cat /mnt/projetos/deploy-be/dynamo/app/globoesporte/current/dynamogloboesporte/version.txt'}
            },
        'dynamo':
            {'dev01':{'hostname':'riovld121.globoi.com','username':'dynamo','pass':'dynamo','cmd':'cat /mnt/projetos/deploy-be/dynamo01/app/globoesporte/current/dynamo/version.txt'},
            'qa01':{'hostname':'riovld122.globoi.com','username':'dynamo','pass':'dynamo','cmd':'cat /mnt/projetos/deploy-be/dynamo01/app/globoesporte/current/dynamo/version.txt'},
            'staging':{'hostname':'riovlb13.globoi.com','username':'watcher','pass':'watch654','cmd':'cat /mnt/projetos/deploy-be/dynamo/app/globoesporte/current/dynamo/version.txt'},
            u'produção':{'hostname':'riolb176.globoi.com','username':'watcher','pass':'b2-4ac','cmd':'cat /mnt/projetos/deploy-be/dynamo/app/globoesporte/current/dynamo/version.txt'}
            },
        'sede':
            {'dev01':{'hostname':'riovld109.globoi.com','username':'sede','pass':'sede','cmd':'cat /mnt/projetos/deploy-be/sede/current/sede/version.txt'},
            'qa01':{'hostname':'riovld110.globoi.com','username':'sede','pass':'sede','cmd':'cat /mnt/projetos/deploy-be/sede/current/sede/version.txt'},
            'staging':{'hostname':'riovlb13.globoi.com','username':'watcher','pass':'watch654','cmd':'cat /mnt/projetos/deploy-be/sede/current/sede/version.txt'},
            u'produção':{'hostname':'riolb176.globoi.com','username':'watcher','pass':'b2-4ac','cmd':'cat /mnt/projetos/deploy-be/sede/current/sede/version.txt'}
            },
        'globo-libby':
            {'dev01':{'hostname':'riovld168.globoi.com','username':'watcher','pass':'watch654','cmd':"cat /mnt/projetos/deploy-be/globoesporte01/app/current/projeto-libby/version.txt"},
            'qa01':{'hostname':'riovld170.globoi.com','username':'watcher','pass':'watch654','cmd':"cat /mnt/projetos/deploy-be/globoesporte01/app/current/projeto-libby/version.txt"},
            'staging':{'hostname':'riovlb25.globoi.com','username':'watcher','pass':'watch654','cmd':"cat /mnt/projetos/deploy-be/globoesporte/app/current/projeto-libby/version.txt"},
            u'produção':{'hostname':'riomp20lb12.globoi.com','username':'watcher','pass':'watch654','cmd':"cat /mnt/projetos/deploy-be/globoesporte/app/current/projeto-libby/version.txt"}
            },
        'colaborativo':
            {'dev01':{'hostname':'riovld168.globoi.com','username':'watcher','pass':'watch654','cmd':"cat /mnt/projetos/deploy-be/globoesporte01/app/current/colaborativo/version.txt"},
            'qa01':{'hostname':'riovld170.globoi.com','username':'watcher','pass':'watch654','cmd':"cat /mnt/projetos/deploy-be/globoesporte01/app/current/colaborativo/version.txt"},
            'staging':{'hostname':'riovlb25.globoi.com','username':'watcher','pass':'watch654','cmd':"cat /mnt/projetos/deploy-be/globoesporte/app/current/colaborativo/version.txt"},
            u'produção':{'hostname':'riomp20lb12.globoi.com','username':'watcher','pass':'watch654','cmd':"cat /mnt/projetos/deploy-be/globoesporte/app/current/colaborativo/version.txt"}
            },
        'dicionario':
            {'dev01':{'hostname':'riovld168.globoi.com','username':'watcher','pass':'watch654','cmd':"cat /mnt/projetos/deploy-be/globoesporte01/app/current/dicionario/version.txt"},
            'qa01':{'hostname':'riovld170.globoi.com','username':'watcher','pass':'watch654','cmd':"cat /mnt/projetos/deploy-be/globoesporte01/app/current/dicionario/version.txt"},
            'staging':{'hostname':'riovlb25.globoi.com','username':'watcher','pass':'watch654','cmd':"cat /mnt/projetos/deploy-be/globoesporte/app/current/dicionario/version.txt"},
            u'produção':{'hostname':'riomp20lb12.globoi.com','username':'watcher','pass':'watch654','cmd':"cat /mnt/projetos/deploy-be/globoesporte/app/current/dicionario/version.txt"}
            },
        'compressor':
            {'dev01':{'hostname':'riovld168.globoi.com','username':'watcher','pass':'watch654','cmd':"rpm -qa *compress*  | sed -e 's/^.*_globo-//;s/\.el[0-9]//'"},
            'qa01':{'hostname':'riovld170.globoi.com','username':'watcher','pass':'watch654','cmd':"rpm -qa *compress* | sed -e 's/^.*_globo-//;s/\.el[0-9]//'"},
            'staging':{'hostname':'riovlb25.globoi.com','username':'watcher','pass':'watch654','cmd':"rpm -qa *compress* | sed -e 's/^.*_globo-//;s/\.el[0-9]//'"},
            u'produção':{'hostname':'riomp20lb12.globoi.com','username':'watcher','pass':'watch654','cmd':"rpm -qa *compress* | sed -e 's/^.*_globo-//;s/\.el[0-9]//'"}
            },
        }