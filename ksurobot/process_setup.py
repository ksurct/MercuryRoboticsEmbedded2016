import logging.config
from setproctitle import setproctitle
import signal


def process_setup():
    exitcmd = lambda *_: exit(0)
    signal.signal(signal.SIGINT, exitcmd)
    signal.signal(signal.SIGTERM, exitcmd)
    setproctitle('ksurctrobot')

    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'long': {
                'format':
                    '%(relativeCreated)d %(threadName)-12s  %(levelname)-5s %(name)-20s %(message)s'
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
            'ksurobot': {
                'propagate': False,
                'handlers': ['console'],
                'level': logging.DEBUG,
            },
            'websockets.server': {
                'propagate': False,
                'handlers': ['console'],
                'level': logging.DEBUG,
            },
        },
        'root': {
            'handlers': ['console'],
            'level': logging.INFO,
        },
    })
