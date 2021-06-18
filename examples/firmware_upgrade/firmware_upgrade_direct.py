from intersight.model.iam_account import IamAccount
from intersight.api import iam_api
from intersight.model.softwarerepository_authorization import SoftwarerepositoryAuthorization
from intersight.model.firmware_eula import FirmwareEula
from intersight.api import firmware_api
from intersight.api import softwarerepository_api
from examples.authentication import client
from intersight.exceptions import NotFoundException
from intersight.model.compute_physical_relationship import ComputePhysicalRelationship
from intersight.api import compute_api
from intersight.model.firmware_upgrade import FirmwareUpgrade
from intersight.model.firmware_direct_download import FirmwareDirectDownload
from intersight.model.firmware_network_share import FirmwareNetworkShare
from intersight.model.firmware_distributable_relationship import FirmwareDistributableRelationship
import intersight
import sys
import re
from pprint import pprint

api_key = "api_key"
api_key_file = "~/api_key_file_path"

api_client = client.get_api_client(api_key, api_key_file)


def get_account_moid():
    api_instance = iam_api.IamApi(api_client)

    try:
        # get a 'IamApi' resource.
        resp_get_iam = api_instance.get_iam_account_list()
        pprint(resp_get_iam)
        return resp_get_iam.results[0].account_moid
    except intersight.ApiException as e:
        print("Exception when calling IamApi->: get_iam_account_list"
              "%s\n" % e)
        sys.exit(1)


def set_auth():
    api_instance = softwarerepository_api.SoftwarerepositoryApi(api_client)

    # Creation of softwareRepository model instance.
    software_repository = SoftwarerepositoryAuthorization()

    software_repository.set_attribute("repository_type", "Cisco")
    software_repository.set_attribute("user_id", "user_id")
    software_repository.set_attribute("password", "password")

    try:
        # create a 'softwareRepositoryAuthorization' resource.
        resp_set_software_rep = api_instance.create_softwarerepository_authorization(software_repository)
        pprint(resp_set_software_rep)
        return resp_set_software_rep
    except intersight.ApiException as e:
        print("Exception when calling SoftwareRepository->: create_softwarerepository_authorization"
              "%s\n" % e)
        sys.exit(1)


def check_auth():
    api_instance = softwarerepository_api.SoftwarerepositoryApi(api_client)

    try:
        # The program assumes that only one softwarerepository Authorization exists.
        # get a 'softwareRepository' resource.
        resp_get_software_rep = api_instance.get_softwarerepository_authorization_list()
        pprint(resp_get_software_rep)
        if resp_get_software_rep.results:
            return True
        else:
            return False
    except intersight.ApiException as e:
        print("Exception when calling SoftwareRepository->: get_softwarerepository_authorization_list"
              "%s\n" % e)
        sys.exit(1)


def check_eula(account_moid):
    api_instance = firmware_api.FirmwareApi(api_client)

    try:
        # get a 'firmwareApi' resource.
        resp_get_firmware_eula = api_instance.get_firmware_eula_by_moid(account_moid)
        pprint(resp_get_firmware_eula)
        return resp_get_firmware_eula.accepted
    except intersight.ApiException as e:
        if re.search('Not Found', e.reason):
            return False
        else:
            print("Exception when calling FirmwareApi->: get_firmware_eula_by_moid %s" % e)
            sys.exit(1)


def set_eula():
    api_instance = firmware_api.FirmwareApi(api_client)

    # create an FirmwareEula model instance
    firmware_eula = FirmwareEula()

    try:
        # create a 'firmwareApi' resource.
        resp_set_firmware_eula = api_instance.create_firmware_eula(firmware_eula)
        pprint(resp_set_firmware_eula)
        return resp_set_firmware_eula
    except intersight.ApiException as e:
        print("Exception when calling FirmwareApi->: create_firmware_eula %s" % e)
        sys.exit(1)


def get_assigned_server():
    # Creating the compute instance api.
    compute_api_instance = compute_api.ComputeApi(api_client)

    # Getting the list of compute rack unit.
    compute_api_response = compute_api_instance.get_compute_rack_unit_list()

    # Handling error scenario if get_compute_rack_unit_list does not return any entry.
    if not compute_api_response.results:
        raise NotFoundException(reason="The response does not contain any entry for compute rack unit."
                                       "Please connect a compute rack unit and then attach the server profile.")

    # Selecting the first compute rack unit to attach the server profile.
    # Fetching the moid.
    rack_unit_moid = compute_api_response.results[0].moid

    # Creation of compute physical relationship object.
    # This instance contains moid of chosen rack unit.
    return ComputePhysicalRelationship(class_id="mo.MoRef",
                                       object_type="compute.RackUnit",
                                       moid=rack_unit_moid)


def check_firmware(server_moid):
    api_instance = firmware_api.FirmwareApi(api_client)

    fltr = "Ancestors.Moid eq '{0}'".format(server_moid)

    # create a 'firmwareApi' resource.
    try:
        resp_firmware = api_instance.get_firmware_running_firmware_list(filter=fltr)
        pprint(resp_firmware)
        return resp_firmware
    except intersight.ApiException as e:
        print("Exception when calling FirmwareApi->: get_firmware_running_firmware_list %s" % e)
        sys.exit(1)


def get_software_image_dist():
    api_instance = firmware_api.FirmwareApi(api_client)
    upgrade_server_model = "UCSC-C240-M4S2"
    image_version = "4.1(3b)"
    fltr = "SupportedModels in ('{0}') and Version eq '{1}' and Tags.Key eq '{2}' " \
           "and Tags.Value eq '{3}'".format(
            upgrade_server_model, image_version, "cisco.meta.distributabletype", "Cisco")

    # create a 'firmwareApi' resource.
    try:
        resp_get_sw_image_dist = api_instance.get_firmware_distributable_list(filter=fltr)
        pprint(resp_get_sw_image_dist)
        return resp_get_sw_image_dist
    except intersight.ApiException as e:
        print("Exception when calling FirmwareApi->: get_firmware_distributable_list %s" % e)
        sys.exit(1)


def update_server_firmware(assigned_server, sw_dist_moid):
    api_instance = firmware_api.FirmwareApi(api_client)

    # FirmwareUpgrade | The 'firmware.Upgrade' resource to create.
    firmware_upgrade = FirmwareUpgrade()

    # Setting all the attributes for firmware_upgrade instance.
    firmware_upgrade.set_attribute("direct_download", FirmwareDirectDownload(
        upgradeoption="upgrade_mount_only"
    ))
    firmware_upgrade.set_attribute("network_share", FirmwareNetworkShare())
    firmware_upgrade.set_attribute("upgrade_type", "direct_upgrade")
    firmware_upgrade.set_attribute("server", assigned_server)
    firmware_upgrade.set_attribute("distributable", FirmwareDistributableRelationship(
        object_type="firmware.Distributable",
        class_id="mo.MoRef",
        moid=sw_dist_moid
    ))

    try:
        # create a 'firmwareApi' resource.
        resp_firmware_upgrade = api_instance.create_firmware_upgrade(firmware_upgrade)
        pprint(resp_firmware_upgrade)
        return resp_firmware_upgrade
    except intersight.ApiException as e:
        print("Exception when calling FirmwareApi->: create_firmware_upgrade %s" % e)
        sys.exit(1)


if __name__ == "__main__":
    # Get the account_moid to set Eula to true.
    account_moid = get_account_moid()

    # Check whether authorization for software repository is set.
    # If not set set it.
    if check_auth():
        print("Auth profile already exists.")
    else:
        set_auth()
        print("Auth profile set successfully.")

    # Check if the Eula is set for the account.
    # If not set to True, set it.
    if check_eula(account_moid):
        print("Eula for account %s is already set" % account_moid)
    else:
        print("Eula for account %s is not set" % account_moid)
        set_eula()

    # Get assigned server.
    assigned_server = get_assigned_server()

    # Get firmware image distributable moid details.
    # We are choosing an image supported for UCSC-C240-M4S2 server
    # and with release "4.1(3b)" and with tag key cisco.meta.distributabletype
    # and tag value as Cisco.
    sw_image_dist = get_software_image_dist()

    # Upgrade the server firmware using upgrade type as direct_upgrade.
    sw_fw_upgrade = update_server_firmware(assigned_server, sw_image_dist.results[0].moid)
