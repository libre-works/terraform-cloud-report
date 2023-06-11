import logging

from typing import List
from classes.api.paginated import Paginated
from classes.api.rest import Rest
from classes.time.datetime import Datetime
from models.dataclasses import TerraformWorkspace, TerraformRun, TerraformProject
 

class Terraform:


    __content_type = "application/vnd.api+json"


    def __init__(self, token, url)  -> None:
        self.token = token
        self.url = url
        self.paginated = Paginated()
        self.datetime = Datetime()
        self.rest = Rest()


    def __del__(self) -> None:
        pass
         

    def get_project(self, project_id ) -> TerraformProject:          

        url = f"{self.url}/api/v2/projects/{project_id}"

        results = self.rest.get(
            url = url,
            content_type = self.__content_type, 
            token = self.token
        )        
        
        project = TerraformProject()
        project.id = project_id
        project.name = results['data']['attributes']['name']

        return project


    def get_workspaces(self, organization) -> List[TerraformWorkspace]:        

        url = f"{self.url}/api/v2/organizations/{organization}/workspaces"

        results = self.paginated.get(
            url = url,
            content_type = self.__content_type, 
            token = self.token
        )

        workspaces = []

        for result in results:
            workspace = TerraformWorkspace()            
            workspace.id = result['id']
            workspace.name = result['attributes']['name']
            workspace.organization = organization
            workspace.project_id = result['relationships']['project']['data']['id']
            # populate !!!
            workspace.configuration_item = ""
            workspaces.append(workspace)
              
            logging.error(f"[workspace]: name: {workspace.name}, project id: {workspace.project_id}")
            logging.error(f"[workspace]: project_name: {workspace.project_name} ")

        return workspaces


    def get_runs(self, workspace: TerraformWorkspace ) -> List[TerraformRun]:
        url = f"{self.url}/api/v2/workspaces/{workspace.id}/runs"
        
        results = self.paginated.get(
            url = url,
            content_type = self.__content_type, 
            token = self.token
        )

        runs = []

        for result in results:
            run = TerraformRun()
            run.id = result['id']
            run.date = result['attributes']['created-at']            
            run.status = result['attributes']['status'] 
            run.age = int(self.datetime.age_days( date = run.date ))
            run.workspace = workspace.name
            run.project_name = workspace.project_name
            run.configuration_item = workspace.configuration_item
            run.cost_center = workspace.cost_center
            logging.info(f"[run]: got run: {str(run)}")
            runs.append(run)

        return runs
