from tornado.ioloop import IOLoop
from . import logger

import functools
import requests


class OandaStreamListener(object):
    def __init__(self, access_token, environment, io_loop=None, max_buffer_size=None,
                 read_chunk_size=None):
        self.io_loop = io_loop
        self.max_buffer_size = max_buffer_size
        self.read_chunk_size = read_chunk_size

        if environment == 'practice':
            self.api_url = 'https://stream-fxpractice.oanda.com'
        elif environment == 'live':
            self.api_url = 'https://stream-fxtrade.oanda.com'
        else:
            raise Exception("Bad environment selected: {}".format(environment))

        self.access_token = access_token
        self.client = requests.Session()
        self.client.stream = True

        if self.access_token:
            self.client.headers['Authorization'] = 'Bearer '+self.access_token

    def listen_stream(self, endpoint="v1/prices", ignore_heartbeat=True, params=None):

        if self.io_loop is None:
            self.io_loop = IOLoop.current()

        params = params or dict()
        params['ignore_heartbeat'] = ignore_heartbeat

        request_args = dict()
        request_args['params'] = params

        url = '%s/%s' % (self.api_url, endpoint)
        print("Will connect to {} with args {}".format(url, request_args))
        connection = self.client.get(url, **request_args)

        callback = functools.partial(self._handle_connection, connection)
        self.io_loop.add_handler(connection.raw.fileno(), callback, self.io_loop.READ)

    def handle_stream(self, stream, device):
        raise NotImplementedError()

    def _handle_connection(self, connection, fd, event):
        try:
            #if connection.status_code != 200:
            #    self.on_error(connection.content)

            for line in connection.iter_lines():
                if line:
                    future = self.handle_stream(line, self.client)
                    if future is not None:
                        self.io_loop.add_future(future, lambda f: f.result())
        except:
            logger.error("Error in connection callback", exc_info=True)
