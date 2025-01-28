import boto3  # type: ignore
from io import BytesIO 

class S3Obj:

    def __init__(self) -> None:
        self.client = boto3.client("s3")
        pass

    def getFile(self, bucketName: str, objfile: str):
        response = self.client.get_object(Bucket=bucketName, Key=objfile)
        file = response["Body"].read()
        return BytesIO(file)
