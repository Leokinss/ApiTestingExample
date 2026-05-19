from locust import HttpUser, task

"""
Load testing example using Locust library
cd into the loadTests directory
run command: locust
It will start a web interface at http://localhost:8089 where you can configure the number of users, spawn rate, and target host to start the load test.

run headless command: locust --headless -u 100 -r 10 -t 1m --host https://restful-booker.herokuapp.com
This will run a load test with 100 users, spawning 10 users per second, for a duration of 1 minute against the specified host. Adjust the parameters as needed for your testing scenario.
"""

class TestUser(HttpUser):
    host = "https://restful-booker.herokuapp.com"

    @task
    def ping(self):
        self.client.get("/ping")