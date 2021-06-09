from examples.authentication import client

from intersight.api import boot_api
from intersight.model.boot_precision_policy import BootPrecisionPolicy
from intersight.model.boot_device_base import BootDeviceBase
from intersight.model.organization_organization_relationship import OrganizationOrganizationRelationship
from pprint import pprint
import intersight

api_key = "api_key"
api_key_file = "~/api_key_file_path"

api_client = client.get_api_client(api_key, api_key_file)


def create_boot_sdcard():
    # Creating an instance of boot_hdd_device
    boot_sdcard = BootDeviceBase(class_id="boot.SdCard",
                                 object_type="boot.SdCard",
                                 name="sdcard1",
                                 enabled=True)
    return boot_sdcard


def create_boot_iscsi():
    # Creating an instance of boot_iscsi
    boot_iscsi = BootDeviceBase(class_id="boot.Iscsi",
                                object_type="boot.Iscsi",
                                name="iscsi1",
                                enabled=True)
    return boot_iscsi


def create_boot_pxe():
    # Creating an instance of boot_pxe
    boot_pxe = BootDeviceBase(class_id="boot.Pxe",
                              object_type="boot.Pxe",
                              name="pxe1",
                              enabled=True,
                              interface_name="pxe1")
    return boot_pxe


def get_boot_precision_policy(api_client):
    # Enter a context with an instance of the API client
    with api_client:
        # Create an instance of the API class
        api_instance = boot_api.BootApi(api_client)

        # example passing only required values which don't have defaults set
        # and optional values
        try:
            # Read a 'boot.PrecisionPolicy' resource.
            api_response = api_instance.get_boot_precision_policy_list()
        except intersight.ApiException as e:
            print("Exception when calling BootApi->get_boot_precision_policy_list: %s\n" % e)
    return api_response


def create_organization(moid):
    # Creating an instance of organization
    organization = OrganizationOrganizationRelationship(class_id="mo.MoRef",
                                                        object_type="organization.Organization",
                                                        moid=moid)

    return organization


# Create an instance of the API class.
api_instance = boot_api.BootApi(api_client)

# Getting the response for existing object.
response = get_boot_precision_policy(api_client)

# Handling error scenario if get_boot_precision_policy does not return any entry.
if not response.results:
    raise NotFoundException(reason="The response does not contain any entry for boot precision policy. "
                                   "Please create a boot precision policy and then update it.")

# Fetch the organization Moid and boot precision policy moid from the Result's first entry.
organization_moid = response.results[0].organization['moid']
moid = response.results[0].moid

# Create an instance of hdd_device, iscsi, pxe, organization and list of boot_devices.
boot_hdd_device = create_boot_sdcard()
boot_iscsi = create_boot_iscsi()
boot_pxe = create_boot_pxe()
organization = create_organization(organization_moid)
boot_devices = [
    boot_hdd_device,
    boot_iscsi,
    boot_pxe,
]

# BootPrecisionPolicy | The 'boot.PrecisionPolicy' resource to create.
boot_precision_policy = BootPrecisionPolicy()

# Setting all the attributes for boot_precison_policy instance.
boot_precision_policy.set_attribute("name", "updated_boot_policy1")
boot_precision_policy.set_attribute("description", "Updated boot precision policy")
boot_precision_policy.set_attribute("boot_devices", boot_devices)
boot_precision_policy.set_attribute("organization", organization)

# example passing only required values which don't have defaults set
try:
    # Update a 'boot.PrecisionPolicy' resource.
    api_response = api_instance.update_boot_precision_policy(
        boot_precision_policy=boot_precision_policy,
        moid=moid)
    pprint(api_response)
except intersight.ApiException as e:
    print("Exception when calling BootApi->update_boot_precision_policy: %s\n" % e)
