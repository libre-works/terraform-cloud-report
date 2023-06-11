import logging

from classes.api.rest import Rest


class Paginated:


    def __init__(self):
        self.rest = Rest()


    def __del__(self):
        pass


    def get(self, 
            url = "",
            content_type = "application/json",
            token = ""):

        results = []

        result = self.rest.get(url = url, 
            content_type = content_type, 
            token = token )

        total_pages = result['meta']['pagination']['total-pages']

        for page in range(1, total_pages + 1):
            
            result = self.rest.get(url = f"{url}?page[number]={page}", 
                content_type = content_type, 
                token = token )

            for item in result['data']:                
                results.append(item) 

            logging.info(f"pagination: Current: {result['meta']['pagination']['current-page']}")

        return results
