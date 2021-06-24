from examples.authentication import client
from intersight.model.server_profile import ServerProfile
from intersight.api import server_api
from intersight.model.policy_abstract_policy_relationship import PolicyAbstractPolicyRelationship
from intersight.model.storage_disk_group_policy import StorageDiskGroupPolicy
from intersight.model.mo_tag import MoTag
from intersight.model.storage_span_group import StorageSpanGroup
from intersight.model.storage_local_disk import StorageLocalDisk
from intersight.model.storage_storage_policy import StorageStoragePolicy
from intersight.model.storage_virtual_drive_config import StorageVirtualDriveConfig
from intersight.api import storage_api
from intersight.model.firmware_server_configuration_utility_distributable import \
    FirmwareServerConfigurationUtilityDistributable
from intersight.model.firmware_server_configuration_utility_distributable_relationship import \
    FirmwareServerConfigurationUtilityDistributableRelationship
from intersight.model.softwarerepository_file_server import SoftwarerepositoryFileServer
from intersight.model.softwarerepository_operating_system_file import SoftwarerepositoryOperatingSystemFile
from intersight.model.softwarerepository_catalog_relationship import SoftwarerepositoryCatalogRelationship
from intersight.model.softwarerepository_operating_system_file_relationship import \
    SoftwarerepositoryOperatingSystemFileRelationship
from intersight.api import softwarerepository_api
from intersight.api import firmware_api
from intersight.model.os_answers import OsAnswers
from intersight.model.organization_organization_relationship import OrganizationOrganizationRelationship
from intersight.model.compute_physical_relationship import ComputePhysicalRelationship
from intersight.api import compute_api
from intersight.model.os_install import OsInstall
from intersight.api import os_api
from intersight.exceptions import NotFoundException
from pprint import pprint
import intersight
import sys

api_key = "api_key"
api_key_file = "~/api_key_file_path"

api_client = client.get_api_client(api_key, api_key_file)


def create_organization():
    # Creating and returning an instance of organization
    return OrganizationOrganizationRelationship(class_id="mo.MoRef",
                                                object_type="organization.Organization")


def create_policy_reference(policy_moid, obj_type):
    return PolicyAbstractPolicyRelationship(moid=policy_moid,
                                            object_type=obj_type,
                                            class_id="mo.MoRef")


def create_catalog(catalog_result):
    moid = catalog_result.results[0].moid
    obj_type = catalog_result.results[0].object_type
    class_id = catalog_result.results[0].class_id
    return SoftwarerepositoryCatalogRelationship(
        class_id="mo.MoRef",
        object_type=obj_type,
        moid=moid
    )


def create_server_profile():
    api_instance = server_api.ServerApi(api_client)

    # Create an instance of organization.
    organization = create_organization()

    # ServerProfile | The 'server.Profile' resource to create.
    server_profile = ServerProfile()

    # Setting all the attributes for server_profile instance.
    server_profile.name = "sample_storage_server_profile1"
    server_profile.description = "sample server profile."
    server_profile.organization = organization

    tags = [
        MoTag(key="profile",
              value="storage_profile")
    ]

    server_profile.tags = tags

    # example passing only required values which don't have defaults set
    try:
        # Create a 'server.Profile' resource.
        resp_server_profile = api_instance.create_server_profile(server_profile)
        pprint(resp_server_profile)
        return resp_server_profile
    except intersight.ApiException as e:
        print("Exception when calling ServerApi->create_server_profile: %s\n" % e)
        sys.exit(1)


def create_disk_group_policy():
    resp_dg_policy_lst = []
    for index in range(2):
        api_instance = storage_api.StorageApi(api_client)

        # Create an instance of organization.
        organization = create_organization()

        # diskGroupPolicy | The 'storage.DiskGroupPolicy' resource to create.
        dg_policy = StorageDiskGroupPolicy()

        # Setting all the attributes for dg_policy instance.
        dg_policy.name = f"sample_dg_policy_raid%d" % index
        dg_policy.description = f"sample disk group policy for raid%d." % index
        dg_policy.organization = organization

        tags = [
            MoTag(key="dg",
                  value="dg_policy")
        ]

        dg_policy.tags = tags
        dg_policy.use_jbods = True
        dg_policy.raid_level = f"Raid%d" % index

        if resp_dg_policy_lst:
            span_groups = StorageSpanGroup(disks=[
                StorageLocalDisk(slot_number=index + 1),
                StorageLocalDisk(slot_number=index + 2),
            ]
            )
            dg_policy.dedicated_hot_spares = [
                StorageLocalDisk(slot_number=index + 3)
            ]
        else:
            span_groups = StorageSpanGroup(disks=[
                StorageLocalDisk(slot_number=index + 1)
            ]
            )

        dg_policy.span_groups = [span_groups]
        # example passing only required values which don't have defaults set
        try:
            # Create a 'storage.DiskGroupPolicy' resource.
            resp_dg_policy = api_instance.create_storage_disk_group_policy(dg_policy)
            pprint(resp_dg_policy)
            resp_dg_policy_lst.append(resp_dg_policy)
        except intersight.ApiException as e:
            print("Exception when calling StorageApi->create_storage_disk_group_policy: %s\n" % e)
            sys.exit(1)
    return resp_dg_policy_lst


def create_virtual_drives(dg_policy_moid_list):
    result = []
    for index, moid in zip(range(2), dg_policy_moid_list):
        if result:
            size = 100
        else:
            size = 102400
        result.append(StorageVirtualDriveConfig(
            name=f"vdrive%d" % index,
            size=size,
            disk_group_policy=moid,
            access_policy="ReadWrite",
            read_policy="Default",
            write_policy="AlwaysWriteBack",
            io_policy="Direct",
            drive_cache="Enable",
            expand_to_available=False,
            boot_drive=False
        ))
    return result


def create_storage_policy(dg_policy_moid):
    api_instance = storage_api.StorageApi(api_client)

    # Create an instance of organization.
    organization = create_organization()

    # StorageStoragePolicy | The 'storage.StoragePolicy' resource to create.
    storage_policy = StorageStoragePolicy()

    # Setting all the attributes for server_profile instance.
    storage_policy.name = "sample_storage_policy1"
    storage_policy.description = "sample storage policy."
    storage_policy.organization = organization

    tags = [
        MoTag(key="policy",
              value="storage")
    ]

    storage_policy.tags = tags
    storage_policy.retain_policy_virtual_drives = False
    storage_policy.unused_disks_state = "UnconfiguredGood"

    virtual_drives = create_virtual_drives(dg_policy_moid)
    storage_policy.virtual_drives = virtual_drives

    # example passing only required values which don't have defaults set
    try:
        # Create a 'storage.StoragePolicy' resource.
        resp_storage_policy = api_instance.create_storage_storage_policy(storage_policy)
        pprint(resp_storage_policy)
        return resp_storage_policy
    except intersight.ApiException as e:
        print("Exception when calling StorageApi->:create_storage_storage_policy %s\n" % e)
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
    assigned_server = ComputePhysicalRelationship(class_id="mo.MoRef",
                                                  object_type="compute.RackUnit",
                                                  moid=rack_unit_moid)

    return assigned_server


def attach_server_to_profile(server_profile_moid):
    api_instance = server_api.ServerApi(api_client)

    # Creation of server profile model instance.
    server_profile = ServerProfile()

    # Fetch assigned server detail
    assigned_server = get_assigned_server()

    # Setting the attribute for server profile with assigned server and server profile moid.
    server_profile.assigned_server = assigned_server

    # example passing only required values which don't have defaults set
    try:
        # Patching a 'Server.Profile' resource.
        resp_server_profile = api_instance.patch_server_profile(moid=server_profile_moid,
                                                                server_profile=server_profile)
        pprint(resp_server_profile)
        return resp_server_profile
    except intersight.ApiException as e:
        print("Exception when calling ServerApi->patch_server_profile: %s\n" % e)
        sys.exit(1)


def deploy_server_profile(server_profile_moid):
    api_instance = server_api.ServerApi(api_client)

    # Creation of server profile model instance.
    server_profile = ServerProfile()

    # Setting the attribute for server profile with the action and server profile moid.
    server_profile.action = "Deploy"

    # example passing only required values which don't have defaults set
    try:
        # Patching a 'Server.Profile' resource.
        resp_server_profile = api_instance.patch_server_profile(moid=server_profile_moid,
                                                                server_profile=server_profile)
        pprint(resp_server_profile)
        return resp_server_profile
    except intersight.ApiException as e:
        print("Exception when calling ServerApi->patch_server_profile: %s\n" % e)
        sys.exit(1)


def attach_policies_to_profile(policy_mapping, server_profile_moid):
    policy_bucket = []

    for obj_type, moid in policy_mapping.items():
        policy = create_policy_reference(moid, obj_type)
        policy_bucket.append(policy)

    api_instance = server_api.ServerApi(api_client)

    # ServerProfile | The 'server.Profile' resource to create.
    server_profile = ServerProfile()

    # Setting all the attributes for server_profile instance.
    server_profile.policy_bucket = policy_bucket

    # example passing only required values which don't have defaults set
    try:
        # Patch a 'server.Profile' resource.
        resp_server_profile = api_instance.patch_server_profile(moid=server_profile_moid,
                                                                server_profile=server_profile)
        pprint(resp_server_profile)
        return resp_server_profile
    except intersight.ApiException as e:
        print("Exception when calling ServerApi->patch_server_profile: %s\n" % e)
        sys.exit(1)


def get_catalog_moid():
    # Create an instance of the API class
    api_instance = softwarerepository_api.SoftwarerepositoryApi(api_client)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Read a 'software.RepositoryApi' resource.
        api_response = api_instance.get_softwarerepository_catalog_list()
        return api_response
    except intersight.ApiException as e:
        print("Exception when calling SoftwarerepositoryApi->get_softwarerepository_catalog_list: %s\n" % e)
        sys.exit(1)


def fetch_os_config_file(config_file="ESXi6.5ConfigFile"):
    # Create an instance of the API class
    api_instance = os_api.OsApi(api_client)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Read a 'os.Api' resource.
        # Fetching the result with the configuration file.
        api_response = api_instance.get_os_configuration_file_list(filter=f"Name eq '%s'" % config_file)
        return api_response
    except intersight.ApiException as e:
        print("Exception when calling OsApi->get_os_configuration_file_list: %s\n" % e)
        sys.exit(1)


def create_osdu_image(catalog):
    api_instance = firmware_api.FirmwareApi(api_client)

    # Creation of firmware_server_config_utility_dist model instance.
    firmware_server_config_utility_dist = FirmwareServerConfigurationUtilityDistributable()

    # Setting the attribute for firmware_server_config_utility_dist.
    firmware_server_config_utility_dist.name = "firmware_server_config_utility_dist1"
    firmware_server_config_utility_dist.version = "s"
    firmware_server_config_utility_dist.supported_models = ["s"]
    firmware_server_config_utility_dist.source = SoftwarerepositoryFileServer(
        object_type="softwarerepository.CifsServer",
        class_id="softwarerepository.CifsServer",
        file_location="10.10.10.20/iso.iso",
        username="user",
        password="password"
    )

    firmware_server_config_utility_dist.catalog = catalog

    # example passing only required values which don't have defaults set
    try:
        # Creating a 'firmware.ServerConfigurationUtilityDistributable' resource.
        resp_fw_server_config_util_dist = api_instance. \
            create_firmware_server_configuration_utility_distributable(
            firmware_server_config_utility_dist
        )
        pprint(resp_fw_server_config_util_dist)
        return resp_fw_server_config_util_dist
    except intersight.ApiException as e:
        print(
            "Exception when calling FirmwareApi->create_firmware_server_configuration_utility_distributable: %s\n" % e)
        sys.exit(1)


def create_os_image(catalog):
    api_instance = softwarerepository_api.SoftwarerepositoryApi(api_client)

    # Creation of SoftwarerepositoryOperatingSystemFile model instance.
    sw_repo_os_file = SoftwarerepositoryOperatingSystemFile()

    # Setting the attribute for firmware_server_config_utility_dist.
    sw_repo_os_file.name = "sw_repo_os_file1"
    sw_repo_os_file.description = "software repository operating System file"
    sw_repo_os_file.vendor = "VMware"
    sw_repo_os_file.version = "ESXi 6.7 U3"
    sw_repo_os_file.source = SoftwarerepositoryFileServer(
        object_type="softwarerepository.CifsServer",
        class_id="softwarerepository.CifsServer",
        file_location="10.10.10.20/iso.iso",
        username="user",
        password="password",
        remote_share="share",
        remote_file="iso.iso",
        remote_ip="10.10.10.10"
    )

    sw_repo_os_file.catalog = catalog

    # example passing only required values which don't have defaults set
    try:
        # Creating a 'softwarerepository.OperatingSystemFile' resource.
        resp_sw_repo_os_file = api_instance. \
            create_softwarerepository_operating_system_file(sw_repo_os_file)
        pprint(resp_sw_repo_os_file)
        return resp_sw_repo_os_file
    except intersight.ApiException as e:
        print("Exception when calling SoftwarerepositoryApi->create_softwarerepository_operating_system_file: %s\n" % e)
        sys.exit(1)


def os_install(os_moid, osdu_moid):
    api_instance = os_api.OsApi(api_client)

    # Creation of OsInstall model instance.
    os_install = OsInstall()

    # Create an instance of organization.
    organization = create_organization()

    os_install.name = "sample_os_install_tempalate1"
    os_install.description = "sample os install tempalate1"
    os_install.install_method = "vMedia"
    os_install.organization = organization
    server = get_assigned_server()
    os_install.server = server
    os_install.image = SoftwarerepositoryOperatingSystemFileRelationship(
        class_id="mo.MoRef",
        object_type="softwarerepository.OperatingSystemFile",
        moid=os_moid
    )
    os_install.osdu_image = FirmwareServerConfigurationUtilityDistributableRelationship(
        class_id="mo.MoRef",
        object_type="firmware.ServerConfigurationUtilityDistributable",
        moid=osdu_moid
    )

    ip_configuration = OsIpConfiguration(object_type="os.Ipv4Configuration",
                                         class_id="os.Ipv4Configuration",
                                         ip_v4_config=CommIpV4Interface(
                                             ip_address="10.10.10.100",
                                             netmask="255.255.255.0",
                                             gateway="10.10.10.1"
                                         ))
    answers = OsAnswers(source="Template",
                        hostname="host1",
                        ip_config_type="static",
                        root_password="ChangePassword",
                        is_root_password_crypted=False,
                        nameserver="10.10.10.1",
                        ip_configuration=ip_configuration,
                        )
    os_install.answers = answers

    fetch_os_config_file_list = fetch_os_config_file()
    os_config_file_moid = fetch_os_config_file_list.results[0].moid

    os_install.configuration_file = OsConfigurationFileRelationship(
        object_type="os.ConfigurationFile",
        class_id="mo.MoRef",
        moid=os_config_file_moid
    )

    # example passing only required values which don't have defaults set
    try:
        # Create a 'os.Install' resource.
        resp_os_install = api_instance.create_os_install(os_install)
        pprint(resp_os_install)
        return resp_os_install
    except intersight.ApiException as e:
        print("Exception when calling OsApi->:create_os_install %s\n" % e)
        sys.exit(1)


if __name__ == "__main__":
    # 1. Create 2 Disk Group Policies and get the policy moid
    dg_policy_raid0, dg_policy_raid1 = create_disk_group_policy()
    dg_policy_raid0_moid = dg_policy_raid0.moid
    dg_policy_raid1_moid = dg_policy_raid1.moid

    # 2. Create new Storage Policy and get the policy moid.
    storage_policy_response = create_storage_policy(
        [dg_policy_raid0_moid,
         dg_policy_raid1_moid]
    )
    storage_policy_response_moid = storage_policy_response.moid

    # 3. Create new server profile and get the profile moid
    server_profile_response = create_server_profile()
    server_profile_moid = server_profile_response.moid

    # 4. Assign the policy to the profile and verify it using restApi
    # Creating a policy mapping with object Type as key and moid will be value.
    policies = {
        "storage.StoragePolicy": storage_policy_response_moid
    }

    # attach the profile to policies
    attach_policies_to_profile(policies, server_profile_moid)

    # assign a server to the server profile
    attach_server_to_profile(server_profile_moid)

    # 5. Deploy the Profile to server.
    deploy_server_profile(server_profile_moid)

    # 6. Create Osimage and Osdu Image.

    # get catalog moid and create catalog
    catalog_moid = get_catalog_moid()
    catalog = create_catalog(catalog_moid)

    os_image_resp = create_os_image(catalog)
    osdu_image_resp = create_osdu_image(catalog)

    # Fetch os and osdu image moid
    os_image_moid = os_image_resp.moid
    osdu_image_moid = osdu_image_resp.moid

    # 7. Install file based os on designated server
    os_install(os_image_moid, osdu_image_moid)
