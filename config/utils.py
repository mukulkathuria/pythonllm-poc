import os
import sys
import re
import json
from datetime import datetime

# import requests  # type: ignore
import random


current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

from data.trained_data import (
    # selected_model_data,
    # requirements_data,
    # make_data,
    # brand_data,
    preferences_data,
    # age_range_data,
    # primary_usage_data,
)


def getBudgetRange(text: str):
    match = re.search(r"(\d+)([kK]?)[- ]?(\d+)([kK]?)", text)
    if match:
        low, low_unit, high, high_unit = match.groups()
        numbers = [int(low), int(high)]
        for i in range(2):
            if numbers[i] in ("k", "K"):
                numbers[i] = 1000
            else:
                numbers[i] = int(numbers[i]) * (
                    1000 if (low_unit or high_unit) in ("k", "K") else 1
                )
        return numbers
    return None


# def getPrefrences(preferences: list, paramsvalue: any, token: str):
#     url = os.environ["similarpreferenceurl"]
#     params = {
#         "preferences": "luxurry,navigati,safety",
#         "make": paramsvalue["make"],
#         "brand": paramsvalue["brand"],
#         "provider": paramsvalue["provider"],
#         "model": "gpt-3.5-turbo-1106%27",
#     }
#     headers = {"Authorization": token}
#     strs = ""
#     for i in range(len(preferences)):
#         if preferences[i]["preference"] and i < len(preferences) - 1:
#             strs += preferences[i]["preference"] + ", "
#         elif preferences[i]["preference"]:
#             strs += preferences[i]["preference"]
#     # res = [
#     #     {"preference_input": "performance", "preference_output": "performance"},
#     #     {"preference_input": "safety", "preference_output": "advance_safety_features"},
#     # ]
#     params["preferences"] = strs if len(strs) > 1 else "luxurry,navigati,safety"
#     res = []
#     data = requests.get(url=url, params=params, headers=headers)
#     if data.status_code == 200:
#         res = json.loads(data.text)
#     else:
#         print(
#             "Status code: {statuscode}. Error Message: {errmsg}. Preferences for: {preferences}".format(
#                 statuscode=data.status_code,
#                 errmsg=data.text,
#                 preferences=str(preferences),
#             )
#         )
#     result = []
#     for i in range(len(res)):
#         result.append(res[i]["preference_output"])
#     return result


def changeDateTime(createddated):
    dateobj = datetime.fromtimestamp(float(createddated) / 1000)
    date = dateobj.strftime("%Y-%m-%d %H:%M:%S")
    weekday = dateobj.weekday()
    is_weekend = 1 if weekday >= 5 else 0
    return {"date": date, "is_weekend": is_weekend}


def addMissingValues(objvalue):
    data_obj = objvalue
    total_chat_time = round(data_obj["total_chat_time"] / 60000, 2)
    data_obj["car_price"] = int(data_obj["car_price"])
    dates = changeDateTime(data_obj["test_drive_date"])
    data_obj["is_weekend"] = dates["is_weekend"]
    data_obj["visited_models"] = len(data_obj["visited_models"].split(","))
    data_obj["initial_budget"] = int(data_obj["initial_budget"])
    data_obj["final_budget"] = int(data_obj["final_budget"])
    if(total_chat_time < 3):
        data_obj["total_chat_time"] = 0
    elif total_chat_time >=3 and total_chat_time <=7:
        data_obj["total_chat_time"] = 1
    else:
        data_obj["total_chat_time"] = 2
    preferencearr = []
    for values in data_obj["preferences"].split(","):
        if values in preferences_data:
            preferencearr.append(values)
        else:
            preferencearr.append("extra")

    for requirements in preferences_data:
        alreadyPresent = False
        for prefrences in preferencearr:
            if prefrences == requirements:
                alreadyPresent = True
        if "extra" in preferencearr:
            data_obj["extra"] = 1
        else:
            data_obj["extra"] = 0

        if alreadyPresent:
            data_obj[requirements] = 1
        else:
            data_obj[requirements] = 0
    keys_to_delete = ["test_drive_date", "preferences", "id"]
    for keys in keys_to_delete:
        data_obj.pop(keys, None)
    return data_obj


def getRandomValue(min: int, max: int):
    return random.randrange(min, max)
