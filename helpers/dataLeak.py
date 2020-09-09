import requests
import logging
import re
import json

logging.basicConfig(level=logging.INFO)

base_url = "http://localhost:5000"


def search_id(userid):
    url = f"{base_url}?userid={userid}"

    logging.info(f"sending {userid}")
    result: requests.Response = requests.get(url)

    if result.status_code == 404:
        logging.info("got 404")
        return None

    logging.info("got result")
    return result.json()['phone_number']


def search_username(username):
    url = f"{base_url}?username={username}"

    logging.info(f"sending {username}")
    result: requests.Response = requests.get(url)

    if result.status_code == 404:
        logging.info("got 404")
        return None

    logging.info("got result")
    return result.json()['phone_number']


def send_to_database(userid, phone, username):
    url = f"{base_url}/new"

    payload = {
        'userid': userid,
        'username': username,
        'phone': phone
    }

    result: requests.Response = requests.post(url, json=payload)

    if result.status_code == 409:
        return True

    return False


def get_data_from_phone(number):
    url = f"http://88.218.17.207/num.php?number={number}"

    try:

        res: requests.Response = requests.get(url)
        json = res.json()

        names = []
        families = []
        cities = []
        addresses = []


        if json['Count'] == 0:
            return names, families, cities, addresses

        for key in json:
            if str(key)[:-1] == "Name":
                names.append(json[key])

            if str(key)[:-1] == "Family":
                families.append(json[key])

            if str(key)[:-1] == "City":
                cities.append(json[key])

            if str(key)[:-1] == "Address":
                addresses.append(json[key])

            
        return names, families, cities, addresses

    except Exception as error:
        logging.warning(error)
