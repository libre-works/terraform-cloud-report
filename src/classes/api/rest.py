import requests
import time

class Rest:

  
    def __init__(self):
        pass


    def __del__(self):
        pass


    def get( self,     
            url = "",
            content_type = "application/json",
            token = "",
            wait_time = 0.1 ):
        
        time.sleep(wait_time)
        headers = {}
        headers['Content-Type'] = content_type
        headers['Authorization'] = f"Bearer {token}"

        data = requests.get (
            url,
            headers = headers,
        )

        result = data.json()

        return result


    def post(self,
            url = "",
            content_type = "application/json",
            token = "" ):

        headers = {}
        headers['Content-Type'] = content_type
        headers['Authorization'] = f"Bearer {token}"

        response = requests.post(
            url,
            headers = headers
        )
