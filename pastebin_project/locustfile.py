from locust import HttpUser, task, between, constant, LoadTestShape
import random
import json
import psutil
import time
from locust import events

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("Starting resource monitoring...")
    environment.runner.stats.csv_writer_interval = 1  # Xuất log mỗi giây

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("Stopping resource monitoring...")

@events.request.add_listener
def on_request_success(request_type, name, response_time, response_length, **kwargs):
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    print(f"CPU: {cpu_usage}%, RAM: {ram_usage}%")


class PastebinUser(HttpUser):
    host = "http://127.0.0.1:8000"
    wait_time = between(1, 3)

    def on_start(self):
        """Lấy CSRF Token trước khi gửi request"""
        response = self.client.get("/")
        if "csrftoken" in response.cookies:
            self.csrf_token = response.cookies["csrftoken"]
        else:
            self.csrf_token = None

    @task(3)
    def get_pastes(self):
        response = self.client.get("/pastes/")
        if response.status_code == 200:
            print("Lấy danh sách paste thành công!")

    @task(2)
    @task
    def create_paste(self):
        """Gửi request có kèm CSRF token"""
        paste_data = {
            "title": f"Test Paste {random.randint(1, 1000)}",
            "content": "Đây là nội dung thử nghiệm",
            "expiration_time": "10m"
        }

        headers = {
            "X-CSRFToken": self.csrf_token,  # Thêm CSRF Token vào header
            "Content-Type": "application/json"
        }

        response = self.client.post("/pastes/", data=json.dumps(paste_data), headers=headers)

        # if response.status_code == 201:
        #     print(f"Created paste: {response.json()}")
        # else:
        #     print(f"Failed to create paste: {response.status_code} - {response.text}")

class CustomLoadShape(LoadTestShape):

    stages = [
        {"duration": 30, "users": 10, "spawn_rate": 2},
        {"duration": 60, "users": 50, "spawn_rate": 5},
        {"duration": 90, "users": 100, "spawn_rate": 10},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
        return None


