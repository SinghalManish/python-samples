from datetime import datetime
from threading import Thread

from device_id_to_vin_mapper import MapDeviceIDWithVIN
from package_handler import PackageHandler
from read_deployment_details import DeploymentExtractor
from read_deployment_log import DeploymentLogAnalyzer
from read_project_configuration import ParseProjectConfiguration
from read_rollout_information import ReadRolloutAttributes

PROJECT = "bajaj"


# def threaded_data_analysis(device_id_vin_handler, key):
#     counter = 1
#     response_data = device_id_vin_handler.read_devices_based_on_rollout_id(key)
#     for key1, value1 in response_data.items():
#         device_id = value1.get("device_id")
#         if device_id in list(valid_vin_device_id_mapping.keys()):
#             print(counter, key1, value1, device_id)
#             counter += 1


if __name__ == "__main__":
    current_timestamp = datetime.now().strftime("%B %dth, %Y %H:%M:%S IST")
    with open("production_dataset.csv", "w") as fp:
        fp.write("Script Start Time :   {}\n".format(str(current_timestamp)))

    configuration_handler = ParseProjectConfiguration(project=PROJECT)
    configuration_attributes = configuration_handler.read_configuration_file
    print("Configuration read")

    # rollout_attribute_handler = ReadRolloutAttributes(configuration_attributes=configuration_attributes)
    # rollout_details = rollout_attribute_handler.read_rollout_information_from_the_cloud

    device_id_vin_handler = MapDeviceIDWithVIN(configuration_attributes=configuration_attributes)
    response = device_id_vin_handler.read_devices_from_cloud
    print("VIN read")

    package_handler = PackageHandler(configuration_attributes=configuration_attributes)
    package_data = package_handler.get_package_set_based_on_package_group
    print("Package read")

    deployment_handler = DeploymentExtractor(configuration_attributes=configuration_attributes)

    deployment_log_handler = DeploymentLogAnalyzer(configuration_attributes=configuration_attributes)

    #valid_vin_device_id_mapping = {}
    if PROJECT == "bajaj":
        with open("production_dataset.csv", "w") as fp:
            fp.write("Sl No;VIN;ECU Under Test;Deployment Status;Deployment start time;Deployment end time\n")
        counter = 1
        device_counter = 1
        for key, value in response.items():
            try:
                print(f"Device {device_counter} / {len(response)}   :   {key}")
                if int(key[-5:]) > 5000 and key[-5:] not in ["05935", "05936"]:
                    #valid_vin_device_id_mapping.update({value: key})
                    # Thread(target=deployment_handler.extract_deployments_for_device_id,
                    #        args=(value, counter, package_data, key, deployment_log_handler)).start()
                    deployment_handler.extract_deployments_for_device_id(
                        device_id=value, counter=counter, package_data=package_data,
                        vin=key, deployment_log_handler=deployment_log_handler)
                    counter += 1
            except ValueError:
                pass
            device_counter += 1

    # with open("production_dataset.csv", "a") as fp:
    #     fp.write("Sl No;VIN;ECU Under Test;Deployment Status;Deployment start time;Deployment end time\n")
    #     counter = 1
    #     for key, value in rollout_details.items():
    #         response_data = device_id_vin_handler.read_devices_based_on_rollout_id(key, valid_vin_device_id_mapping)
    #         if response_data:
    #             for key1, value1 in response_data.items():
    #                 deployment_status_response = None
    #                 package_id = value1.get("package_id")
    #                 deployment_status = value1.get("deployment_status")
    #                 deployment_start, deployment_end = deployment_log_handler.get_deployment_start_end_time(key1)
    #                 if package_data.get(package_id):
    #                     package_data_formatted = "_".join(package_data.get(package_id))
    #                 else:
    #                     package_data_formatted = "Not Available"
    #                 if deployment_status in ["UPDATE_COMPLETED", "UPDATE_FAILED"]:
    #                     deployment_status_response = deployment_log_handler.read_deployment_log(key1)
    #                 deployment_status = deployment_status_response if deployment_status_response else deployment_status
    #                 data_to_write = [str(counter),
    #                                  valid_vin_device_id_mapping[response_data.get(key1).get("device_id")],
    #                                  package_data_formatted, deployment_status, str(deployment_start),
    #                                  str(deployment_end)]
    #                 Thread(target = write_to_file, args = (fp, data_to_write)).start()
    #                 print(data_to_write)
    #                 counter += 1
    print(datetime.now().strftime("%Y-%b-%D %H:%M:%S"))
