import requests
from datetime import datetime
import time
import schedule

base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
api_url_telegram = "https://api.telegram.org/bot1815767434:AAGV9MgnoNKlOB_F6RaUIGzvcxmE3NGxEgA/sendMessage?chat_id=@__groupid__&text="
group_id = "demo_telegram_cowin_2"
delhi_district_ids = [140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150]
# delhi_district_ids = [141]


def fetch_data_from_cowin(district_id):
    query_params = "?district_id={}&date={}".format(district_id, today_date)
    final_url = base_cowin_url + query_params
    response = requests.get(final_url)
    extract_availability_data(response)


def fetch_data_for_state(district_ids):
    for district_id in district_ids:
        fetch_data_from_cowin(district_id)


def extract_availability_data(response):
    response_json = response.json()
    i = 0
    for center in response_json["centers"]:
        i = i + 1
        if i > 5:
            break
        message = ""
        for session in center["sessions"]:
            if session["available_capacity_dose1"] > 0 and session["min_age_limit"] == 18:
                message += "Pincode: {}, \nName: {}, \nSlots: {}, \nDate: {}, \nVaccine: {}, \nFee Type: {}, \nMinimum Age: {} \n----\n".format(
                    center["pincode"], center["name"],
                    session["available_capacity_dose1"],
                    session["date"],
                    session["vaccine"],
                    center["fee_type"],
                    session["min_age_limit"]
                )

        send_message_telegram(message)


def send_message_telegram(message):
    final_telegram_url = api_url_telegram.replace("__groupid__", group_id)
    final_telegram_url = final_telegram_url + message
    response = requests.get(final_telegram_url)
    print(response.json())


if __name__ == '__main__':
    schedule.every(10).seconds.do(lambda: (fetch_data_for_state(delhi_district_ids)))
    while True:
        schedule.run_pending()
        time.sleep(1)
