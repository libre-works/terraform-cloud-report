from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class Slack:
    

    def __init__(self, token,):                           
        self.client = WebClient(token = token)
 
      
    def __del__(self):
        pass  
  
                        
    def post_file(self, comment, file_name, channel):
        try:
            self.client.files_upload(
                channels = channel,
                initial_comment = comment,
                file = file_name,
              )
        except SlackApiError as e:
            assert e.response["error"]
