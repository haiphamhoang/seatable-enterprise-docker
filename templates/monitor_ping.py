import os
import sys
import requests


TIMEOUT = int(os.getenv('DTABLE_SERVER_PING_TIMEOUT', 20))
DTABLE_SERVER_PING_URL = 'http://127.0.0.1:5000/ping/'
DTABLE_WEB_PING_URL = 'http://127.0.0.1:8000/api2/ping/'
DTABLE_DB_PING_URL = 'http://127.0.0.1:7777/ping/'

"""
requests.exceptions.ConnectionError
requests.exceptions.ReadTimeout

if raise Exception, the py script's return_code != 0
"""


def ping(url):
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code, response.text


if __name__ == '__main__':
    if len(sys.argv) == 2:
        name = sys.argv[1]

        if name == 'dtable-server':
            ping(DTABLE_SERVER_PING_URL)

        elif name == 'dtable-web':
            ping(DTABLE_WEB_PING_URL)

        elif name == 'dtable-db':
            ping(DTABLE_DB_PING_URL)

        else:
            pass
