from dataclasses import dataclass, field
from dataclass_wizard import JSONListWizard, JSONWizard


@dataclass 
class CostCenterResponse(JSONListWizard):
    name: str = ""
    Items: list['CostCenterRelation'] = field(default_factory=list)


@dataclass 
class CostCenterRelation:
    configuration_item: str = ""
    cost_center: str = ""


@dataclass
class TerraformProject:
    name: str = ""
    id: str = ""


@dataclass
class TerraformRun:
    age: int = 0
    date: str = ""
    workspace: str = ""
    project_name: str = ""
    status: str = ""
    id: str = ""
    configuration_item: str = ""
    cost_center: str = ""


@dataclass
class TerraformWorkspace:
    name: str = ""
    id: str = ""
    organization:  str = ""
    project_id: str = ""
    project_name: str = "" 
    configuration_item: str = ""
    cost_center: str = ""


@dataclass
class Config(JSONWizard):
    organization: str
    url:  str
    age: int
    channel: str
    comment: str
    db_table: str
    db_file: str
    db_key: str
    wait_time: float
