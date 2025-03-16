import time
import psutil


def test_homepage_performance():
    with app.test_client() as client:
        start_time = time.time()
        response = client.get('/')
        end_time = time.time()

        assert response.status_code == 200
        assert end_time - start_time < 1  # Checking, if response get lower than 1 second

# def test_homepage_resource_loading():
#     with zpi_app.test_client() as client:
#         response = client.get('/')
#
#         assert response.status_code == 200
#         assert b'<link' in response.data  # Check if CSS files are loaded
#         assert b'<script' in response.data  # Check if JavaScript files are loaded
#         assert b'<img' in response.data  # Check if images are loaded


def test_homepage_memory_usage():
    with app.test_client() as client:
        # Measure memory usage during page load
        # In this example, We're using the psutil library, which needs to be installed before usage: pip install psutil

        response = client.get('/')
        process = psutil.Process()

        assert response.status_code == 200
        assert process.memory_info().rss / (1024 ** 2) < 100  # Check if memory usage is less than 100 MB

# Add other tests from the list above depending on your application's specifics
