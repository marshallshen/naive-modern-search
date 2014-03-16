import unittest
import httpretty
import requests

from nose.tools import *
from app.freebase import FreebaseClient

JSON_RESPONSE = '{"status":"200 OK","result":[{"mid":"/m/041h0","id":"/en/j_r_r_tolkien","name":"J. R. R. Tolkien","notable":{"name":"Author","id":"/book/author"},"lang":"en","score":71.052925}]}'
def test_http_requests():
    httpretty.enable()  # enable HTTPretty so that it will monkey patch the socket module

    test_url = 'https://www.googleapis.com/freebase/v1/search?query=tolkien&key=account_key'
    httpretty.register_uri(httpretty.GET, test_url,
                         body=JSON_RESPONSE,
                         content_type="application/json")
    response = FreebaseClient('account_key').search('tolkien')
    expected_response = [{u'lang': u'en', u'name': u'J. R. R. Tolkien', u'notable': {u'name': u'Author', u'id': u'/book/author'}, u'mid': u'/m/041h0', u'score': 71.052925, u'id': u'/en/j_r_r_tolkien'}]

    assert_equal(response, expected_response)
    httpretty.disable()
    httpretty.reset()

