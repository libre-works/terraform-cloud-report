import boto3


class AWSBase:


    def __init__(self, 
            service: str, 
            region: str, 
            profile: str):     
          
        self.service = service
        self.region = region
        self.profile = profile
 
 
    def __del__(self):
        pass
   

    def create_client(self) -> boto3.client:

        session = boto3.Session( profile_name = self.profile, 
                region_name = self.region )
    
        client = session.client(self.service )
        
        return client  


    def create_resource(self) -> boto3.resource:
        session = boto3.Session( profile_name = self.profile, 
                region_name = self.region )
    
        resource = session.resource(self.service)

        return resource
