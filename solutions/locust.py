from locust.env import Environment
from locust import HttpUser, task, between
from locust.stats import stats_history, RequestStats
import gevent

class MainUser(HttpUser):
    host = "http://172.22.103.131:3000"

    def on_start(self):
        credentials = {
            "Identity": "admin",
            "secret": "adminpw1"
        }
        with self.client.post("/login", json=credentials, name="Get /login", catch_response=True) as resp:
            self.token = resp.json()["token"]
            self.cookies = dict(resp.cookies)
            self.headers = {
                "cookie": self.cookies,
                "Authorization": f"Bearer {self.token}"
            }

    @task
    def post_wheelsets(self):
        data = {
        "axle_eq": 1,
        "axle_num": "111117",
        "cancel_condition": 5,
        "cancel_date": "2019-08-17T14:16:02+03:00",
        "cancel_num": 1,
        "car_defect": 107,
        "country": 20,
        "customer_inn": 5009093400,
        "customer_kpp": 770101001,
        "customer_name": "ООО \"РегионТрансСервис\"",
        "data_source": "torek",
        "detail_tag": 4,
        "document_date": "2019-08-17",
        "document_number": 1445,
        "document_type": 22,
        "full_examin_plant": "0344",
        "gost": "ГОСТ",
        "income_date": "2019-07-14",
        "income_depot": 4108,
        "inv_items_char": "Толщина обода: 9",
        "inv_items_name": "ПАРА КОЛЕСНАЯ",
        "manufacturer": "0005",
        "op_code": 9,
        "operation_date": "2020-01-09",
        "operation_place": 4108,
        "outcome_date": "2019-07-17",
        "owner_inn": 5009093400,
        "owner_kpp": 770101001,
        "owner_name": "ООО \"РегионТрансСервис\"",
        "receipt_date": "2019-08-17",
        "receipt_source": 2,
        "recipient_inn": 5009093400,
        "recipient_kpp": 770101001,
        "recipient_name": "ООО \"РегионТрансСервис\"",
        "repair_type": "ТР2",
        "rim_thickness_range": 9,
        "sender_inn": 7708503727,
        "sender_mark": 4108,
        "sender_name": "ВЧД-6-Санкт-Петербург",
        "serial": "0005-004584-07",
        "source_name": 95314902,
        "state": 6,
        "storage_address": "193174, Санкт-Петербург, Сортировочная Московская 23/1",
        "storage_number": "ВЧД-6-Санкт-Петербург МППВ",
        "storage_type": 1,
        "transportation_type": 3,
        "updatedAt": 1578563892892,
        "wheel_defect": 117,
        "wheel_side": 1,
        "wheels": [],
        "ws_defect": 117,
        "ws_type": 1,
        "year_build": "07",
        "CHANGEDATE": "2020-03-06T13:22:34"
}
        resp = self.client.post("/wheelsets", data=data, name="Post /wheelsets", headers=self.headers, catch_response=True)
        print(resp.status_code)

# def test_getreqstats():
env = Environment(user_classes=[MainUser])
env.create_local_runner()
gevent.spawn(stats_history, env.runner)
env.runner.start(user_count=500, spawn_rate=250)
gevent.spawn_later(10, lambda: env.runner.quit())
env.runner.greenlet.join()
print(f'''\n"name": {env.stats.total.name},
"num_failures": {env.stats.total.num_failures},
"avg_response_time": {env.stats.total.avg_response_time},
"min_response_time": {env.stats.total.min_response_time},
"max_response_time": {env.stats.total.max_response_time},
"current_rps": {env.stats.total.current_rps},
"median_response_time": {env.stats.total.median_response_time},
"avg_content_length": {env.stats.total.avg_content_length},
"num_requests": {env.stats.total.num_requests}''')
print("stat for posts\n", env.stats.get(name="Post /wheelsets", method="POST"))