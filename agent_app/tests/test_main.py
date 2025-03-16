import unittest
from agent_app.app.main import app  # Import aplikacji Flask

class TestEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index(self):
        response = self.client.post('/add_admin', json={"teacher_name": "admin_test"})
        assert response.status_code == 500

    def test_example_endpoint(self):
        response = self.client.get('/remove_without_folder')

        # it's post endpoint
        assert response.status_code == 405

if __name__ == '__main__':
    unittest.main()
