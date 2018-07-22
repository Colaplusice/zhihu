from pprint import pformat
from wsgiref.simple_server import make_server

def app(environ,start_response):
    headers={'Content-type':'text/plain;charset=utf-8'}
    start_response('200 ok',list(headers.items()))
    yield 'here is the wsgi environment: \r'
    pass