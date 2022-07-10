from datetime import datetime
import requests


class ReadRolloutAttributes:
    def __init__(self, configuration_attributes=None):
        self.configuration_attributes = configuration_attributes
        self.rollout_parameters: dict = {}

    @property
    def read_rollout_information_from_the_cloud(self):
        rollout_request_url = f"{self.configuration_attributes.end_point_url}/rollouts"
        rollout_query = {"limit": 500000, "offset": 0}

        response = requests.get(url=rollout_request_url, headers=self.configuration_attributes.cloud_handler_header,
                                params=rollout_query)
        for data in response.json().get("results"):
            rollout_start_time = None

            rollout_type = data.get("rolloutType")

            if rollout_type == "SOFTWARE_UPDATE":
                device_group_id = data.get("deviceGroupIDs")
                package_id = data.get("packageID")
                rollout_id = data.get("rolloutID")

                self.rollout_parameters.update(
                    {
                        rollout_id:
                            {
                                "device_group_id" : device_group_id,
                                "package_id": package_id,
                            }
                    }
                )

        return self.rollout_parameters
