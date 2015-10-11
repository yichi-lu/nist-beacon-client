#!/usr/bin/env python

#
# A twisted client for NIST beacon
#
# NIST beacon: https://beacon.nist.gov/home
#

import time

from twisted.web.client import getPage
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.web.error import Error
from twisted.internet import reactor

class NIST_beacon(object):
    def __init__(self, url):
        self.baseurl = url

    @inlineCallbacks
    def get_current(self, timestamp):
        result = yield getPage(self.baseurl + timestamp)
        returnValue(result)

    @inlineCallbacks
    def get_previous(self, timestamp):
        result = yield getPage(self.baseurl + 'previous/' + timestamp)
        returnValue(result)

    @inlineCallbacks
    def get_next(self, timestamp):
        result = yield getPage(self.baseurl + 'next/' + timestamp)
        returnValue(result)

    @inlineCallbacks
    def get_last(self):
        result = yield getPage(self.baseurl + 'last')
        returnValue(result)

    @inlineCallbacks
    def get_startchain(self, timestamp):
        result = yield getPage(self.baseurl + 'start-chain/' + timestamp)
        returnValue(result)

@inlineCallbacks
def main():
    beacon = NIST_beacon('https://beacon.nist.gov/rest/record/')

    ttime = time.time()
    ts = str(int(ttime))

    try:
        record = yield beacon.get_current(ts)
    except Error as e:
        print 'Error message from calling beacon.get_current(): %s' % e.message
    else:
        print 'Current record: %s' % record

    try:
        record = yield beacon.get_previous(ts)
    except Error as e:
        print 'Error message from calling beacon.get_previous(): %s' % e.message
    else:
        print 'Previous record: %s' % record

    try:
        record = yield beacon.get_next(ts)
    except Error as e:
        print 'Error message from calling beacon.get_next(): %s' % e.message
    else:
        print 'Next record: %s' % record

    try:
        record = yield beacon.get_last()
    except Error as e:
        print 'Error message from calling beacon.get_last(): %s' % e.message
    else:
        print 'Last record: %s' % (record)

    try:
        record = yield beacon.get_startchain(ts)
    except Error as e:
        print 'Error message from calling beacon.get_startchain(): %s' % e.message
    else:
        print 'Start chain: %s' % record

    reactor.stop()

if __name__ == '__main__':
    main()
    reactor.run()
