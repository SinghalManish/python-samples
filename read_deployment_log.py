import re
from datetime import datetime

import requests


class DeploymentLogAnalyzer:
    def __init__(self, configuration_attributes=None):
        self.configuration_attributes = configuration_attributes
        self.deployment_log_query = {"limit": 20000, "offset": 0}

    def read_deployment_log(self, deployment_id: str = None):
        deployment_status_from_log = None

        deployment_log_url = f"{self.configuration_attributes.end_point_url}/deployments/{deployment_id}/logs"
        response = requests.get(url=deployment_log_url, headers=self.configuration_attributes.cloud_handler_header,
                                params=self.deployment_log_query)

        for log in response.json().get("results"):
            if "UPDATE_SKIPPED" in log.get("text"):
                deployment_status_from_log = "UPDATE SKIPPED"
                break
            elif "Newly polled deployment found, failing current deployment" in log.get("text"):
                deployment_status_from_log = "FAILED DUE TO NEWLY PULLED DEPLOYMENT"
                break
            else:
                deployment_status_from_log = self.check_error_category(log.get("text"))[-1]
                if deployment_status_from_log:
                    break

        return deployment_status_from_log

    def check_error_category(self, error_description):
        is_recoverable_error, error_category, response = True, None, None

        non_recoverable_error = {
            "NVM CORRUPTION": [r".*(primary ECU has ECU ID.*and serial number.*which "
                               r"doesn't match the last known primary ECU)"],
            "UPTANE PROVISIONING": [r".*(message: device is unlocked, reprovisioning "
                                    r"expected)",
                                    r".*(cannot reprovision locked device: resource already "
                                    r"exists)",
                                    r".*(error while verifying version manifest signatures "
                                    r"for device.*could not find key for primary ECU.*)"]
        }

        for error_type, error_list in non_recoverable_error.items():
            for error in error_list:
                response = re.match(error, error_description)
                if response:
                    is_recoverable_error = False
                    break
            if not is_recoverable_error:
                error_category = error_type
                break

        return is_recoverable_error, error_category

    def get_deployment_start_end_time(self, deployment_id:str = None):
        deployment_overview_url = f"{self.configuration_attributes.end_point_url}/deployments/{deployment_id}"
        response = requests.get(url=deployment_overview_url, headers=self.configuration_attributes.cloud_handler_header)

        try:
            deployment_start_time = datetime.strptime(response.json().get("startTime"), "%Y-%m-%dT%H:%M:%SZ")
        except:
            deployment_start_time = "Not Available"

        try:
            deployment_end_time = datetime.strptime(response.json().get("endTime"), "%Y-%m-%dT%H:%M:%SZ")
        except:
            deployment_end_time = "Not Available"

        return deployment_start_time, deployment_start_time
