import logging
import os

from datetime import date 
from litedb import DiskDatabase
from models.dataclasses import TerraformRun, Config
from classes.api.slack import Slack
from classes.data.json import Json

logging.basicConfig(level=logging.NOTSET)

# load config --------------------
json = Json()
config_dict = json.load_file("config.json")
config = Config.from_dict(config_dict)
token = os.environ['SLACK_TOKEN']

# instantiate objects --------------
slack = Slack( token = token )
db = DiskDatabase(config.db_file)

# select the table that contains object of type Run -----------------
records = db.select(TerraformRun)

# for our convenience, look at the indexes we can query on.
indexes = records.indexes
logging.info(f"available indexes are: ${indexes}")

timestamp = date.today().strftime('%Y%m%d')
filename = f"tfc-report-{timestamp}.txt"

# get distinct list of projects containing applied runs --------------- 
results = records.retrieve( status = 'applied', age = (0, config.age))

configuration_items = []
for record in results:
    logging.info(f"found ci: {str(record)}")
    configuration_items.append(record.configuration_item)

configuration_items = list(set(configuration_items))

# create an initial file -------------------------------------------------
file_handler = open(filename, "w")
file_handler.write("project,configuration_item,workspace,applies,cost_center\n")
file_handler.close()
file_handler = open(filename, "a")

for configuration_item in configuration_items:
    results = []

    try:
        results = records.retrieve( 
            status = 'applied', 
            age = (0, config.age), 
            configuration_item = configuration_item )
    except IndexError:
        logging.error(f"index missing for {configuration_item}")

    # write the values to file -----------------------------------------
    total = 0
    project_name = ""
    cost_center = ""
    workspace = ""

    for record in results:
        project_name = record.project_name
        cost_center = record.cost_center
        workspace = record.workspace
        total += 1

    file_handler.write(f"{project_name},{configuration_item},{workspace},{total},{cost_center}\n")

# close file handler now we are done    
file_handler.close()

slack.post_file(
   comment = config.comment ,
   file_name = filename,
   channel = config.channel 
)
