# from flask import Flask
# import zpi_app
#
# # tests examples
# def test_endpoint():
#     with zpi_app.test_client() as client:
#         response = client.get('/my_endpoint')
#         assert response.status_code == 200
#         assert b'Hello World!' in response.data
#
#         assert response.headers['Content-Type'] == 'application/json'
#
#         assert 'key' in response.json()
#         assert response.json()['key'] == 'wartość'
#
#         # checking if endpoint return error if someone....
#         assert response.status_code == 400
#
# def test_authorized_access():
#     with zpi_app.test_client() as client:
#         response = client.get('/protected-endpoint', headers={'Authorization': 'Bearer token_for_admin_user'})
#         assert response.status_code == 200
#         assert response.json()['role'] == 'admin'
#
# def test_unauthorized_access():
#     with zpi_app.test_client() as client:
#         response = client.get('/protected-endpoint', headers={'Authorization': 'Bearer token_for_regular_user'})
#         assert response.status_code == 403  # Expected error code for no permissions
#
# def test_empty_data():
#     with zpi_app.test_client() as client:
#         response = client.post('/data-endpoint', json={})
#         assert response.status_code == 400  # Oczekiwany kod błędu dla pustych danych
#
# def test_extreme_data():
#     with zpi_app.test_client() as client:
#         data = {'value': 'a' * 1000000}  # Przykładowy bardzo długi ciąg znaków
#         response = client.post('/data-endpoint', json=data)
#         assert response.status_code == 200  # Oczekiwany sukces, jeśli dane są obsługiwane poprawnie
#
#
# def test_data_consistency():
#     # Wstaw dane do bazy danych
#     insert_test_data()
#
#     # Pobierz dane za pomocą endpointu
#     response = client.get('/data-endpoint')
#
#     # Porównaj dane zwrócone przez endpoint z danymi w bazie danych
#     assert response.json() == get_expected_data_from_database()
