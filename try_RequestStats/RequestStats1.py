from locust.env import Environment
from locust import HttpUser, task, TaskSet, between
from locust.stats import stats_history, RequestStats, stats_printer
import gevent
from locust.log import setup_logging

# setup_logging("INFO", None)

class MainUser(HttpUser):
    host = "http://172.22.103.131:8081"
    wait_time = between(0, 1)

    @task
    def first_task(self):
        self.client.get("/wheelsets", name="Get /wheelsets")

# def test_getreqstats():
env = Environment(user_classes=[MainUser])
env.create_local_runner()
gevent.spawn(stats_history, env.runner)
env.runner.start(user_count=10, spawn_rate=100, wait=True)
gevent.spawn_later(10, lambda: env.runner.quit())
env.runner.greenlet.join()
print(f'''\n"name": {env.stats.total.name},
"num_failures": {env.stats.total.num_failures},
"avg_response_time": {env.stats.total.avg_response_time},
"min_response_time": {env.stats.total.min_response_time},
"max_response_time": {env.stats.total.max_response_time},
"current_rps": {env.stats.total.current_rps},
"median_response_time": {env.stats.total.median_response_time},
"avg_content_length": {env.stats.total.avg_content_length}''')


