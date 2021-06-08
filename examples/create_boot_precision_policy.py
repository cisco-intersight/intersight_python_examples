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


def create_boot_local_cdd():
    # Creating an instance of boot_local_cdd
    boot_local_cdd = BootDeviceBase(class_id="boot.LocalCdd",
                                    object_type="boot.LocalCdd",
                                    name="local_cdd1",
                                    enable=True)
    return boot_local_cdd


def create_boot_local_disk():
    # Creating an instance of boot_local_disk
    boot_local_disk = BootDeviceBase(class_id="boot.LocalDisk",
                                     object_type="boot.LocalDisk",
                                     name="local_disk1",
                                     enable=True)
    return boot_local_disk

def create_organization():
    # Creating an instance of organization
    organization = OrganizationOrganizationRelationship(class_id="mo.MoRef",
                                            object_type="organization.Organization")

    return organization

# Enter a context with an instance of the API client.
with api_client:
    # Create an instance of the API class.
    api_instance = boot_api.BootApi(api_client)

    # Create an instance of local_cdd, local_disk, organization and list of boot_devices.
    boot_local_cdd = create_boot_local_cdd()
    boot_local_disk = create_boot_local_disk()
    organization = create_organization()
    boot_devices = [
        boot_local_disk,
        boot_local_cdd,
    ]

    # BootPrecisionPolicy | The 'boot.PrecisionPolicy' resource to create.
    boot_precision_policy = BootPrecisionPolicy()

    # Setting all the attributes for boot_precison_policy instance.
    boot_precision_policy.set_attribute("name", "sample_boot_policy1")
    boot_precision_policy.set_attribute("description", "sample boot precision policy")
    boot_precision_policy.set_attribute("boot_devices", boot_devices)
    boot_precision_policy.set_attribute("organization", organization)

    # example passing only required values which don't have defaults set
    try:
        # Create a 'boot.PrecisionPolicy' resource.
        api_response = api_instance.create_boot_precision_policy(boot_precision_policy)
        pprint(api_response)
    except intersight.ApiException as e:
        print("Exception when calling BootApi->create_boot_precision_policy: %s\n" % e)
