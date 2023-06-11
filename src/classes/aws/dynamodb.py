from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from classes.aws.aws_base import AWSBase


class DynamoDB(AWSBase):

    __service = 'dynamodb'

    def __init__(self, region: str, profile: str):
        
        super().__init__( service = self.__service, 
            region = region, 
            profile = profile )
        self.client = self.create_client()
        self.resource = self.create_resource()
  
    
    def put_item(self, 
            table_name: str,
            item: dict ):
        table = self.resource.Table( table_name )
        table.put_item( Item = item )

        return 

    def get_item(self, 
            table_name: str,
            key: str,
            value: str) -> dict:
        
        table = self.resource.Table( table_name )

        response = table.query(
            KeyConditionExpression=Key( key ).eq( value )
        )

        print(str(response))
        return response