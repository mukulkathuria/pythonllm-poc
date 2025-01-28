import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

from data.models import models_data
from config.OpenAIservice import OpenAIService
from config.AwsBedrockService import AwsBedRockService

async def get_similar_vehicle(userinput: str, make: str, brand: str):
    prompt = """You have been provided the list of vehicle models in model_list in JSON format below.
            You need to find the similar model of vehicle model from the 'model_list'. 
            If vehicle model available in model_list then output JSON will be like {model:{model deatils }} else find 
            the vehicle model in model_list which nearest matches with user entered model and 
            return JSON Output like {model:{model deatils}}, still if no record found then strictly return {} in JSON format. Do not add any sentence and stricly return an object as provided in the example.
            model_list = """
    models_query = []
    for i in range(len(models_data)):
        if models_data[i]['make'] == make and models_data[i]['brand'] == brand:
            models_query.append({ "id": models_data[i]['id'], "name": models_data[i]['name'] })
    openaiService = OpenAIService()
    msg = prompt + str(models_query)
    message_history = [
        {"role": "system", "content": msg},
        {"role": "user", "content": userinput},
    ]
    res = await openaiService.respondToMessage(message_history)
    return res


async def get_similar_vehicle_bybedrock(userinput: str, make: str, brand: str):
    prompt = """You have been provided the list of vehicle models in model_list in JSON format below.
            You need to find the similar model of vehicle model from the 'model_list'. 
            If you found name of vehicle then return that object only, 
            you don't need to write any code just search vehicle name out from the list 
            and return the object still if no record found then strictly return {} in JSON format. 
            Do not add any sentence and stricly return an object as provided in the example.
            model_list = """
    models_query = []
    for i in range(len(models_data)):
        if models_data[i]['make'] == make and models_data[i]['brand'] == brand:
            models_query.append({ "id": models_data[i]['id'], "name": models_data[i]['name'] })
    awsbedrockService = AwsBedRockService()
    msg = prompt + str(models_query) + ". User asked to search vehicle of " + userinput
    message_history = [
        {"role": "user", "content": msg},
        # {"role": "assistant", "content": msg},
    ]
    res = awsbedrockService.getPromptResponse(message_history)
    if("data" in res and "suggestedModel" in res["data"]):
        res = res["data"]
    return res
