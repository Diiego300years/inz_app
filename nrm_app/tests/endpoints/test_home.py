from wsgi import application


# Simply test for root /
def test_endpoint():
    with application.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'Hello World!' in response.data
        #
        # assert response.headers['Content-Type'] == 'application/json'
        #
        # assert 'key' in response.json()
        # assert response.json()['key'] == 'value'

        # checking if endpoint return error if....
        # assert response.status_code == 400
