import requests


class MapDeviceIDWithVIN:
    def __init__(self, configuration_attributes=None):
        self.configuration_attributes = configuration_attributes
        self.device_id_to_vin_mapper = {}

    @property
    def read_devices_from_cloud(self):
        device_read_url = f"{self.configuration_attributes.end_point_url}/devices"
        device_read_query = {"limit": 50000, "offset": 0}

        response = \
            requests.get(url = device_read_url, headers=self.configuration_attributes.cloud_handler_header,
                         params=device_read_query)

        for data in response.json().get("results"):
            self.device_id_to_vin_mapper.update({data.get("deviceSerialNumber"): data.get("deviceID")})

        return self.device_id_to_vin_mapper

    def read_devices_based_on_rollout_id(self, rollout_id: str = None, valid_vin_device_id_mapping: dict = None):
        temp_dataset = {}

        rollout_device_list_url = f"{self.configuration_attributes.end_point_url}/rollouts/{rollout_id}/deployments"
        rollout_device_list_query = {"limit" : 65000}

        response = \
            requests.get(url=rollout_device_list_url, headers=self.configuration_attributes.cloud_handler_header,
                         params=rollout_device_list_query)

        for deployment_data in response.json().get("results"):
            deployment_id = deployment_data.get("deploymentID")
            device_id = deployment_data.get("deviceID")
            package_id = deployment_data.get("packageID")
            deployment_status = deployment_data.get("deploymentStatus")

            if device_id in valid_vin_device_id_mapping.keys():
                temp_dataset.update({deployment_id: {"device_id": device_id, "package_id": package_id,
                                                     "deployment_status": deployment_status}})

        return temp_dataset
