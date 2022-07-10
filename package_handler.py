import requests


class PackageHandler:
    def __init__(self, configuration_attributes=None):
        self.configuration_attributes = configuration_attributes
        self.package_group_name = self.configuration_attributes.package_group
        self.component_parameter = self.configuration_attributes.component_parameters
        self.package_group_id = []
        self.package_dataset = {}

    @property
    def get_package_set_based_on_package_group(self):
        package_group_id_url = f"{self.configuration_attributes.end_point_url}/package-groups"
        package_group_query = {"limit": 50, "offset": 0}

        response = requests.get(url=package_group_id_url, headers=self.configuration_attributes.cloud_handler_header,
                                params=package_group_query)

        for data in response.json().get("results"):
            if data.get("packageGroupName") in self.package_group_name:
                self.package_group_id.append(data.get("packageIDs"))

        if self.package_group_id:
            for package_set in self.package_group_id:
                for package_id in package_set:
                    package_set_url = f"{self.configuration_attributes.end_point_url}/packages/{package_id}/package-files"
                    response = requests.get(url=package_set_url,
                                            headers=self.configuration_attributes.cloud_handler_header)
                    response_data = response.json()
                    for data in response_data:
                        package_id = data.get("packageID")
                        file_name = self.get_component_name_from_package_information(data.get("file").get("fileName"))
                        if file_name:
                            if self.package_dataset.get(package_id):
                                self.package_dataset[package_id].append(file_name)
                            else:
                                self.package_dataset.update({package_id: [file_name]})

        return self.package_dataset

    def get_component_name_from_package_information(self, filename: str = None):
        component_mapped_data = None

        for component_name, component_id in self.component_parameter.items():
            if component_id in filename:
                component_mapped_data = component_name
                break

        return component_mapped_data
