from requests import Session
from time import time
from threading import Thread

reqs = 0
cred = {"identity": "admin", "secret": "adminpw1"}
headers = {"Content-Type": "application/json"}

def post_test(numt, timeout):
    sess = Session()
    resp = sess.post(url="http://172.22.103.131:3000/login", json=cred, headers=headers)
    token = resp.json()["token"]
    cookie = {key: value for (key, value) in resp.cookies.iteritems()}
    headers["Authorization"] = "Bearer " + token
    start_time = time()
    for i in range(numt*req_per_thread, (numt+1)*req_per_thread):
        body = {"axle_eq": 1, "axle_num": "{:0>6}".format(str(i)), "cancel_condition": 5,"cancel_date": "2019-08-17T14:16:02+03:00", "cancel_num": 1, "car_defect": 107, "country": 20,"customer_inn": 5009093400, "customer_kpp": 770101001, "customer_name": "ООО\"РегионТрансСервис\"","data_source": "torek", "detail_tag": 4, "document_date": "2019-08-17", "document_number": 1445,"document_type": 22, "full_examin_plant": "0344", "gost": "ГОСТ", "income_date": "2019-07-14","income_depot": 4108, "inv_items_char": "Толщина обода:9", "inv_items_name": "ПАРА КОЛЕСНАЯ","manufacturer": "0005", "op_code": 9, "operation_date": "2020-01-09", "operation_place": 4108,"outcome_date": "2019-07-17", "owner_inn": 5009093400, "owner_kpp": 770101001, "owner_name": "ООО\"РегионТрансСервис\"", "receipt_date": "2019-08-17", "receipt_source": 2, "recipient_inn": 5009093400,"recipient_kpp": 770101001, "recipient_name": "ООО \"РегионТрансСервис\"", "repair_type": "ТР2","rim_thickness_range": 9, "sender_inn": 7708503727, "sender_mark": 4108,"sender_name": "ВЧД-6-Санкт-Петербург", "serial": "0005-004584-07", "source_name": 95314902, "state": 6,"storage_address": "193174,Санкт-Петербург,Сортировочная Московская 23/1","storage_number": "ВЧД-6-Санкт-Петербург МППВ", "storage_type": 1, "transportation_type": 3,"updatedAt": 1578563892892, "wheel_defect": 117, "wheel_side": 1, "wheels": [], "ws_defect": 117,"ws_type": 1, "year_build": "07", "CHANGEDATE": "2020-03-06T13:22:34"}
        resp = sess.post(url="http://172.22.103.131:3000/wheelsets", cookies=cookie, headers=headers, json=body)
        if time() - start_time >= timeout:
            break
    sess.close()
    global reqs
    reqs += i - numt*req_per_thread


thread_num = 50
total_requests = 0
worktime = 5
req_per_thread = int(total_requests / thread_num) if total_requests else int(1000000 / thread_num)
threads=[]
for thr in range(thread_num):
    x = Thread(target=post_test, args=(thr, worktime,))
    threads.append(x)
    x.start()
for thr in threads:
    thr.join()

print(reqs/worktime)