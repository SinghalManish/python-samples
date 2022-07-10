from threading import Thread

import requests


class DeploymentExtractor:
    def __init__(self, configuration_attributes):
        self.configuration_attributes = configuration_attributes

    def extract_deployments_for_device_id(self, device_id: str = None, counter: int = 0,
                                          package_data=None, vin=None, deployment_log_handler=None):
        deployment_read_url = f"{self.configuration_attributes.end_point_url}/devices/{device_id}/deployments"
        deployment_read_query = {"limit": 50000, "offset": 0}

        response = requests.get(url=deployment_read_url, headers=self.configuration_attributes.cloud_handler_header,
                                params=deployment_read_query)

        for deployment in response.json().get("results"):
            if deployment.get("deploymentType") == "SOFTWARE_UPDATE":
                deployment_id = deployment.get("deploymentID")
                deployment_status = deployment.get("deploymentStatus")
                deployment_start_time = deployment.get("startTime")
                deployment_end_time = deployment.get("endTime")
                deployment_package_id = deployment.get("packageID")
                if package_data.get(deployment_package_id):
                    package_data_formatted = "_".join(package_data.get(deployment_package_id))
                else:
                    package_data_formatted = "Not Available"
                if deployment_status in ["UPDATE_COMPLETED", "UPDATE_FAILED"]:
                    deployment_status_response = deployment_log_handler.read_deployment_log(deployment_id)
                    deployment_status = deployment_status_response if deployment_status_response else deployment_status

                print(counter, ";" , vin, ";" , deployment_status)
                data_to_write = ["", vin, package_data_formatted, deployment_status,
                                 str(deployment_start_time), str(deployment_end_time)]
                with open("production_dataset.csv", "a") as file_pointer:
                    file_pointer.write(";".join(data_to_write) + "\n")
