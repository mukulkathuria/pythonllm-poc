import boto3
from botocore.exceptions import ClientError
import json


class AwsBedRockService:
    def __init__(self):
        self.client = boto3.client("bedrock-runtime", region_name="ap-south-1")
        self.model = "anthropic.claude-3-haiku-20240307-v1:0"

    def getPromptResponse(self, prompt):
        try:
            request = json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "messages": prompt,
                    "max_tokens": 512,
                }
            )
            response = self.client.invoke_model(modelId=self.model, body=request)
            model_response = json.loads(response["body"].read())
            result = model_response["content"][0]["text"]
            return {"data": result}
        except (ClientError, Exception) as e:
            return {"error": str(e)}
