# tornado-oanda
[![Build Status](https://travis-ci.org/cpapazaf/tornado-oanda.svg?branch=master)](https://travis-ci.org/cpapazaf/tornado-oanda)

## Overview
Oanda forex trading stream service for tornado web server


##Example Usage

    import tornado.ioloop
    from tornado_oanda import *
    from tornado.gen import coroutine
    
    import logging
    logger = logging.getLogger('tornado_oanda')
    logger.setLevel(logging.DEBUG)
    
    
    @coroutine
    def eur_usd_prices(instrument, bid, ask, time):
        # TODO: do things here
    
    
    @coroutine
    def eur_usd_events(transaction):
        # TODO: do things here
    

    if __name__ == '__main__':
    
        token = ""
        account_id = ""
    
        my_rates = OandaRatesServer([('^EUR_USD$', eur_usd_prices)], 
                                    account_id=account_id, 
                                    access_token=token, 
                                    environment="practice")
        my_rates.listen(instruments="EUR_USD,EUR_SEK")
    
        my_events = OandaEventsServer([('^EUR_USD$', eur_usd_events)], 
                                      account_id=account_id, 
                                      access_token=token, 
                                      environment="practice")
        my_events.listen()
    
        tornado.ioloop.IOLoop.current().start()

## Contribution

### Creating Issues

If you find a problem please create an 
[issue in the ticket system](https://github.com/cpapazaf/tornado-oanda/issues)
and describe what is going wrong or what you expect to happen.
If you have a full working example or a log file this is also helpful.
You should of course describe only a single issue in a single ticket and not 
mixing up several different things into a single issue.

### Creating a Pull Request

Before you create a pull request it is necessary to create an issue in
the [ticket system before](https://github.com/cpapazaf/tornado-oanda/issues)
and describe what the problem is or what kind of feature you would like
to add. Afterwards you can create an appropriate pull request.

It is required if you want to get a Pull request to be integrated into to squash your
commits into a single commit which references the issue in the commit message.

A pull request has to fulfill only a single ticket and should never create/add/fix
several issues in one, cause otherwise the history is hard to read and to understand 
and makes the maintenance of the issues and pull request hard.

## License

Distributed under the Apache License 2.0 license: http://opensource.org/licenses/Apache-2.0
