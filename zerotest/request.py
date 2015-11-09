__author__ = 'Hari Jiang'
from urlparse import urlparse

import requests


class Request(object):
    def __init__(self, scheme=None, method=None, params=None, host=None, path=None, headers=None, data=None):
        self.scheme = scheme
        self.method = method
        self.headers = headers
        self.data = data
        self.params = params
        self.host = host
        self.path = path

    @property
    def endpoint(self):
        return "{scheme}://{host}".format(**self.__dict__)

    @endpoint.setter
    def endpoint(self, endpoint):
        parsed = urlparse(endpoint)
        self.scheme = parsed.scheme
        if parsed.port:
            host = "{}:{}".format(parsed.hostname, parsed.port)
        else:
            host = parsed.hostname
        self.host = host

    @property
    def url(self):
        return "{}{}".format(self.endpoint, self.path)

    def send_request(self, verify=True):
        return requests.request(self.method, self.url, headers=self.headers,
                                params=self.params, data=self.data,
                                stream=True, allow_redirects=False, verify=verify)

    def __str__(self):
        return """[{method}]{url}
{headers}
{data}""".format(method=self.method, url=self.url, headers=self.headers, data=self.data)