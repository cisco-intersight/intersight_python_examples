from intersight.api import firmware_api
from examples.authentication import client
from intersight.exceptions import NotFoundException
from intersight.model.compute_physical_relationship import ComputePhysicalRelationship
from intersight.api import compute_api
from intersight.model.firmware_upgrade import FirmwareUpgrade
from intersight.model.firmware_direct_download import FirmwareDirectDownload
from intersight.model.firmware_network_share import FirmwareNetworkShare
from intersight.model.firmware_cifs_server import FirmwareCifsServer
import intersight
import sys
from pprint import pprint

api_key = "api_key"
api_key_file = "~/api_key_file_path"

api_client = client.get_api_client(api_key, api_key_file)


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


def update_server_firmware(assigned_server):
    api_instance = firmware_api.FirmwareApi(api_client)

    # FirmwareUpgrade | The 'firmware.Upgrade' resource to create.
    firmware_upgrade = FirmwareUpgrade()

    # Setting all the attributes for firmware_upgrade instance.
    firmware_upgrade.set_attribute("direct_download", FirmwareDirectDownload())
    cifs_server = FirmwareCifsServer(
        mount_options="ntlmv2",
        file_location="/file"
    )
    firmware_upgrade.set_attribute("network_share", FirmwareNetworkShare(
        upgradeoption="nw_upgrade_mount_only",
        map_type="cifs",
        username="user1",
        password="password",
        cifs_server=cifs_server
    ))
    firmware_upgrade.set_attribute("upgrade_type", "network_upgrade")
    firmware_upgrade.set_attribute("server", assigned_server)

    try:
        # create a 'firmwareApi' resource.
        resp_firmware_upgrade = api_instance.create_firmware_upgrade(firmware_upgrade)
        pprint(resp_firmware_upgrade)
        return resp_firmware_upgrade
    except intersight.ApiException as e:
        print("Exception when calling FirmwareApi->: create_firmware_upgrade %s" % e)
        sys.exit(1)


if __name__ == "__main__":
    # Get assigned server.
    assigned_server = get_assigned_server()

    # Upgrade the server firmware using upgrade type as network_upgrade.
    sw_fw_upgrade = update_server_firmware(assigned_server)
