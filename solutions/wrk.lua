wrk.body = '{"identity": "admin","secret": "adminpw1"}'
wrk.headers["Content-Type"] = "application/json"
cookie = {}
cookie["ws-cookie"] = "MTY1NzEwNTYyMXxEdi1CQkFFQ180SUFBUkFCRUFBQUpfLUNBQUVHYzNSeWFXNW5EQW9BQ0dsa1pXNTBhWFI1Qm5OMGNtbHVad3dIQUFWaFpHMXBiZz09fDR4l8shMnAWzhilDnbfA0KAHs3Aqul_SOAjN_0YRL9D; Path=/; Expires=Fri, 05 Aug 2022 11:07:03 GMT;"
wrk.headers["Cookie"] = cookie
token = nil
i = 1

itosix = function(i)
    string_i = tostring(i)
    while string.len(string_i) < 6 do
        string_i = 0 .. string_i
    return string_i
    end
end

random_num = function(x)
    return math.random(0, 10^x-1)
end

random_body = function(i)
    math.randomseed(os.time())
    body = '{"axle_eq":1,"axle_num": "' .. itosix(i) .. '","cancel_condition":' .. tostring(random_num(1)) .. ',"cancel_date":"201' .. tostring(random_num(1)) .. '-0' .. tostring(random_num(1)) .. '-1' .. tostring(random_num(1)) .. '(1)T14:16:0' .. tostring(random_num(1)) .. '+03:00","cancel_num":1,"car_defect":' .. tostring(random_num(1)) .. ',"country":20,"customer_inn":' .. tostring(random_num(10)) .. ',"customer_kpp":' .. tostring(random_num(9)) .. ',"customer_name":"","data_source":"torek","detail_tag":' .. tostring(random_num(1)) .. ',"document_date":"2019-08-17","document_number":1445,"document_type":22,"full_examin_plant":"0344","gost":"ГОСТ","income_date":"2019-07-14","income_depot":4108,"inv_items_char":"0","inv_items_name":"wheelset","manufacturer":"0005","op_code":9,"operation_date":"2020-01-09","operation_place":4108,"outcome_date":"2019-07-17","owner_inn":' .. tostring(random_num(10)) .. ',"owner_kpp":' .. tostring(random_num(9)) .. ',"owner_name":"","receipt_date":"2019-08-17","receipt_source":2,"recipient_inn":5009093400,"recipient_kpp":770101001,"recipient_name":"","repair_type":"ТР2","rim_thickness_range":9,"sender_inn":7708503727,"sender_mark":4108,"sender_name":"Saint-Petersburg","serial":"0005-004584-07","source_name":95314902,"state":6,"storage_address":"193174,ss,ss 23/1","storage_number":"55","storage_type":1,"transportation_type":3,"updatedAt":1578563892892,"wheel_defect":117,"wheel_side":1,"wheels":[],"ws_defect":117,"ws_type":1,"year_build":"07","CHANGEDATE":"2020-03-06T13:22:34"}'
    return body
end

request = function()
    if not token then
        return wrk.format("POST", "/login")
    end
    wrk.headers["Content-Length"] = 1505
    return wrk.format("POST", "/wheelsets")
end

response = function(status, headers, body)
    if not token then
        token = string.sub(body, string.find(body, "token")+8, string.find(body, "is_admin")-4)
        wrk.headers["Authorization"] = "Bearer " .. token
        wrk.headers["Cookie"] = headers["Set-Cookie"]
    else
        i = i + 1
        wrk.body = random_body(i)
    end
end