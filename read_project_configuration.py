from dataclasses import dataclass, field
from os.path import dirname, join
from yaml import safe_load


@dataclass
class ProjectAttributes:
    cloud_handler_header: dict = field(default_factory=dict)
    end_point_url: str = None
    package_group: str = None
    component_parameters: dict = field(default_factory=dict)


class ParseProjectConfiguration:
    def __init__(self, project: str = None):
        self.project = project
        self.project_configuration_file = join(dirname(__file__), "project_configuration.yaml")
        self.project_attributes = ProjectAttributes()

    @property
    def read_configuration_file(self):
        configuration_data_content = None

        with open(self.project_configuration_file) as fp:
            configuration_data_content = safe_load(fp).get(self.project)

        self.project_attributes.cloud_handler_header = {
            "X-Master-Api-Key": configuration_data_content.get("api_key", None),
            "X-Master-Api-Secret": configuration_data_content.get("api_secret", None),
            "Content-Type": configuration_data_content.get("content_type", None)
        }
        self.project_attributes.end_point_url = configuration_data_content.get("end_point_url")
        self.project_attributes.package_group = configuration_data_content.get("package_group")
        self.project_attributes.component_parameters = configuration_data_content.get("component_parameters")

        return self.project_attributes
