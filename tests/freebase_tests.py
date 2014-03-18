from __init__ import *
from app.freebase import FreebaseClient

def test_freebase_search():
    httpretty.enable()

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'fixtures/search_result.json')
    fixture_file = open(filename)
    mock_json_response = fixture_file.read()
    fixture_file.close()

    test_url = 'https://www.googleapis.com/freebase/v1/search?query=tolkien&key=account_key'
    httpretty.register_uri(httpretty.GET, test_url,
                         body=mock_json_response,
                         content_type="application/json")
    freebase_client = FreebaseClient('account_key')
    actual_raw_results = freebase_client.search('tolkien')

    assert_equal("/m/041h0", actual_raw_results['result'][0]['mid'])
    assert_equal("/m/0kbl71v", actual_raw_results['result'][-1]['mid'])

    httpretty.disable()
    httpretty.reset()

def test_freebase_topic():
    httpretty.enable()

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'fixtures/topic_result.json')
    fixture_file = open(filename)
    mock_json_response = fixture_file.read()
    fixture_file.close()

    test_url = 'https://www.googleapis.com/freebase/v1/topic/m/041h0?key=account_key'
    httpretty.register_uri(httpretty.GET, test_url,
                         body=mock_json_response,
                         content_type="application/json")

    freebase_client = FreebaseClient('account_key')
    actual_raw_results = freebase_client.topic('/m/041h0')

    assert_equal('/award/award_winner/awards_won', actual_raw_results['property'].keys()[0])
    assert_equal('/book/book_subject/works', actual_raw_results['property'].keys()[-1])

    httpretty.disable()
    httpretty.reset()

def test_freebase_mql():
    httpretty.enable()

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'fixtures/mql_result.json')
    fixture_file = open(filename)
    mock_json_response = fixture_file.read()
    fixture_file.close()

    test_url = 'https://www.googleapis.com/freebase/v1/mqlread?query=%5B%7B%22type%22%3A+%22%2Fbook%2Fauthor%22%2C+%22id%22%3A+null%2C+%22name%22%3A+null%2C+%22%2Fbook%2Fauthor%2Fworks_written%22%3A+%5B%7B%22name%7E%3D%22%3A+%22Lord+Of+Rings%22%2C+%22a%3Aname%22%3A+null%7D%5D%7D%5D&key=account_key'
    httpretty.register_uri(httpretty.GET, test_url,
                         body=mock_json_response,
                         content_type="application/json")

    freebase_client = FreebaseClient('account_key')
    query =  [{ "/book/author/works_written": [{ "a:name": None, "name~=": "Lord Of Rings"}],
                "id": None,
                "name": None,
                "type": "/book/author"
              }]
    actual_raw_results = freebase_client.mql(query)

    assert_equal('J. R. R. Tolkien', actual_raw_results['result'][0]['name'])

    httpretty.disable()
    httpretty.reset()


