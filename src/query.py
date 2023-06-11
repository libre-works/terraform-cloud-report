import logging
import os

from litedb import DiskDatabase
from classes.api.terraform import Terraform
from classes.data.json import Json
from classes.aws.dynamodb import DynamoDB
from models.dataclasses import Config, CostCenterResponse

'''
The purpose of this script is to cache all runs we have in TFE along with useful information
so that we can query the dataset locally using a standard NoSQL DB.
'''

logging.basicConfig(level=logging.NOTSET)

# load configuration
json = Json()
config_dict = json.load_file("config.json")
config = Config.from_dict(config_dict) 

# delete existing DB
logging.info("Removing existing db to cache a fresh dataset -------------")
if os.path.exists(config.db_file):
    os.removedirs(config.db_file)

# initialize objects
db = DiskDatabase(config.db_file)
dynamodb = DynamoDB(
    region = "xxxxxx",
    profile = "xxxxxx"
)

# get api token from env variable -------------
token = os.environ['TFC_TOKEN']

terraform = Terraform(
    url = config.url,
    token = token
)

# get a list of all workspaces -----------------------
workspaces = terraform.get_workspaces ( organization = config.organization )

for workspace in workspaces:

    # set the name the workspace belongs to -----------------------
    project = terraform.get_project( project_id = workspace.project_id )

    # record the project name -------------------------------------
    workspace.project_name = project.name

    # extract configuration item ----------------------------------    
    try:
        seperated_name = workspace.name.split("__")
        configuration_item = seperated_name[1]
    except IndexError:
        logging.error(f"could not determine ci from regexp for {workspace.name}")
    else:
        logging.info(f"got ci: {configuration_item}  from worksapce: {workspace.name}")
        workspace.configuration_item = configuration_item

    # get ci/cost center relationship from dynamodb
    try:
        response = dynamodb.get_item (
            table_name = config.table,
            key = config.db_key,
            value = workspace.configuration_item
        )
        
        # store in workspace data object
        cost_center_response = CostCenterResponse.from_dict(response)
        workspace.cost_center = cost_center_response.Items[0].cost_center   
    except: 
        workspace.cost_center = "unknown"
        logging.error(f"could not determine cost center for: {workspace.name} and ci: {workspace.configuration_item}")

    finally:
        logging.info(f"workspace: {workspace.name},  ci: {workspace.configuration_item},  cost_center: {workspace.cost_center}")
        terraform_runs = terraform.get_runs( workspace = workspace )
    
        for run in terraform_runs:
            db.insert(run)
            db.commit()

