import logging.config
from setproctitle import setproctitle

setproctitle('ksurctrobot')

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'f': {
            'format':
                'log  %(levelname)-8s %(name)-12s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'formatter': 'f',
            'class': 'logging.StreamHandler',
            'level': logging.DEBUG,
        }
    },
    'loggers': {
        'robot': {
            'propagate': False,
            'handlers': ['console'],
            'level': logging.DEBUG,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': logging.DEBUG,
    },
})


from .main import main

main()
