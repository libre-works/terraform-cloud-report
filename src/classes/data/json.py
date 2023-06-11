import json
from json.decoder import JSONDecodeError

class Json:

    def load_file(self, filename) -> dict:

        dictionary = {}   
        try:
            file_handler = open(filename)
            dictionary = json.load(file_handler)
    
        except JSONDecodeError as e:
            print(f"error decoding json file {filename}: {e}")
    
        finally:
            file_handler.close()
    
        return dictionary
   