import time
import requests
from selenium import webdriver
import datetime
import json

"""
Login page
"""
driver = webdriver.Chrome()
driver.get("https://crabeats.realtek.com/Home/Login")

account = driver.find_element("id", "textUserId")
account.send_keys("chungray_tseng")

password = driver.find_element("id", "textPassword")
password.send_keys("/aA19940321")

btn_login = driver.find_element("id", "buttonLogin")
btn_login.click()

"""
check if already login
"""
cookies = []
while not cookies:
    cookies = driver.get_cookies()

cookies_str = ""
for i in range(0, len(cookies)):
    cookies_item_str = cookies[i]["name"] + "=" + cookies[i]["value"] + "; "
    cookies_str += cookies_item_str
request_header = {
    "cookie": cookies_str
}

start_date = datetime.datetime(2022, 11, 14)
end_date = datetime.datetime(2022, 11, 18)
search_day = start_date
order_list = []

while search_day <= end_date:
    search_day_str = search_day.strftime("%Y/%m/%d")
    # sending get request and saving the response as response object
    r = requests.get(
        url="https://crabeats.realtek.com/Food/ListTodayMenus?date={search_day_str}&location=%E7%91%9E%E6%98%B1%E4%B8%80%E5%BB%A0".format(
            search_day_str=search_day_str),
        allow_redirects=False, headers=request_header)
    if r.status_code == 200:
        food_list_json = json.loads(r.text)
        for item in food_list_json:
            if item["VendorName"] == "燒臘-饕爺":
                if "油雞" in item["Name"] or "香腸" in item["Name"] or "叉燒" in item["Name"] or "烤鴨" in item[
                    "Name"] or "大排" in item["Name"]:
                    order_list.append(item)
        search_day += datetime.timedelta(days=1)

"""
GET READY FOR POST DATA
"""
order_list_post_format_data = []
for item in order_list:
    arrive_time_id = "4" if item["Meal"] == "B" else "5"
    data = {
        "Date": item["EffectiveDate"],
        "Meal": item["Meal"],
        "MealId": item["Id"],
        "Location": item["Location"],
        "FloorId": "6",
        "ArriveTimeId": arrive_time_id,
        "Count": "1",
        "MealName": item["Name"],
        "Money": item["Price"]
    }
    order_list_post_format_data.append(data)

for post_data in order_list_post_format_data:
    requests.post("https://crabeats.realtek.com/Food/AddMealRegister", json=post_data, headers=request_header)

