from .oanda_listener import OandaStreamListener
from tornado.gen import coroutine
import re
import json
from . import logger


class OandaRatesServer(OandaStreamListener):

    def __init__(self, handlers, account_id, *args, **kwargs):
        self.handlers = list(handlers or [])
        self.account_id = account_id

        for spec in self.handlers:
            if not isinstance(spec, (tuple, list)):
                raise TypeError("Handler specs must be list or tuple")
            assert len(spec) in (2, 3, 4)

        super(OandaRatesServer, self).__init__(*args, **kwargs)

    def listen(self, instruments="EUR_USD", ignore_heartbeat=True):
        params = dict()
        params['accountId'] = self.account_id
        params['instruments'] = instruments
        self.listen_stream(endpoint="v1/prices", ignore_heartbeat=ignore_heartbeat, params=params)

    @coroutine
    def handle_stream(self, data, device):

        oanda_prices = json.loads(data.decode("utf-8"))
        logger.debug("Got prices: {}".format(oanda_prices))

        if 'heartbeat' in oanda_prices:
            # TODO: handle heartbeats
            pass

        if 'tick' in oanda_prices:
            instrument_data = oanda_prices['tick']
            for spec in self.handlers:
                regular_expression, callback = spec
                match = re.match(regular_expression, instrument_data['instrument'])
                if match:
                    yield callback(instrument_data['instrument'],
                                   instrument_data['bid'],
                                   instrument_data['ask'],
                                   instrument_data['time'])


class OandaEventsServer(OandaStreamListener):

    def __init__(self, handlers, account_id, *args, **kwargs):
        self.handlers = list(handlers or [])
        self.account_id = account_id

        for spec in self.handlers:
            if not isinstance(spec, (tuple, list)):
                raise TypeError("Handler specs must be list or tuple")
            assert len(spec) in (2, 3, 4)

        super(OandaEventsServer, self).__init__(*args, **kwargs)

    def listen(self, ignore_heartbeat=True, **params):
        self.listen_stream(endpoint='v1/events', ignore_heartbeat=ignore_heartbeat, params=params)

    @coroutine
    def handle_stream(self, data, device):

        oanda_events = json.loads(data.decode("utf-8"))
        logger.debug("Got events: {}".format(oanda_events))

        if 'heartbeat' in oanda_events:
            # TODO: handle heartbeats
            pass

        if 'transaction' in oanda_events:
            ot = oanda_events['transaction']
            for spec in self.handlers:
                regular_expression, callback = spec
                match = re.match(regular_expression, ot['instrument'])
                if match:
                    yield callback(ot)
