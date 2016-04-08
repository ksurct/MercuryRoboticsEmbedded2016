import asyncio
import logging

logger = logging.getLogger(__name__)


class AsyncioLoop(object):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.loop.set_exception_handler(self._handle_exception)
        self.exception = None

    def __enter__(self):
        return self

    def __exit__(self, *enc):
        self.loop.run_forever()
        if self.exception:
            raise self.exception

    def _handle_exception(self, loop, context):
        self.loop.stop()
        self.exception = context.get('exception', Exception(context['message']))

    def submit(self, task):
        asyncio.ensure_future(task)


def gi_init():
    sys.path.append('/usr/lib/python3/dist-packages/')
    import gi

    sys.path.pop()


def get_config():
    from ..main import parser
    return parser.parse_args()
