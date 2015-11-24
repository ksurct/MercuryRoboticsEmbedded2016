import logging.config
from setproctitle import setproctitle

setproctitle('ksurctrobot')

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'long': {
            'format': '%(relativeCreated)d %(threadName)-12s  %(levelname)-8s %(name)-12s %(message)s'
        },
        'brief': {
            'format':
                'log %(threadName)-12s  %(levelname)-8s %(name)-12s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'formatter': 'brief',
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
