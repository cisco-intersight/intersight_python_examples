from examples.authentication import client
from intersight.model.server_profile import ServerProfile
from intersight.api import server_api
from intersight.model.policy_abstract_policy_relationship import PolicyAbstractPolicyRelationship
from intersight.model.ntp_policy import NtpPolicy
from intersight.api import ntp_api
from intersight.model.smtp_policy import SmtpPolicy
from intersight.api import smtp_api
from intersight.model.snmp_policy import SnmpPolicy
from intersight.api import snmp_api
from intersight.model.snmp_user import SnmpUser
from intersight.model.organization_organization_relationship import OrganizationOrganizationRelationship
from intersight.model.compute_physical_relationship import ComputePhysicalRelationship
from intersight.api import compute_api
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


def create_server_profile():
    api_instance = server_api.ServerApi(api_client)

    # Create an instance of organization.
    organization = create_organization()

    # ServerProfile | The 'server.Profile' resource to create.
    server_profile = ServerProfile()

    # Setting all the attributes for server_profile instance.
    server_profile.name = "sample_server_profile1"
    server_profile.description = "sample server profile."
    server_profile.organization = organization

    # example passing only required values which don't have defaults set
    try:
        # Create a 'server.Profile' resource.
        resp_server_profile = api_instance.create_server_profile(server_profile)
        pprint(resp_server_profile)
        return resp_server_profile
    except intersight.ApiException as e:
        print("Exception when calling ServerApi->create_server_profile: %s\n" % e)
        sys.exit(1)


def create_ntp_policy():
    api_instance = ntp_api.NtpApi(api_client)

    # Create an instance of organization.
    organization = create_organization()

    # NtpPolicy | The 'ntp.Policy' resource to create.
    ntp_policy = NtpPolicy()

    # Setting all the attributes for server_profile instance.
    ntp_policy.name = "sample_ntp_policy1"
    ntp_policy.description = "sample ntp policy."
    ntp_policy.organization = organization
    ntp_servers = [
        "10.10.10.250", "10.10.10.10", "10.10.10.20", "10.10.10.30"
    ]
    ntp_policy.ntp_servers = ntp_servers

    # example passing only required values which don't have defaults set
    try:
        # Create a 'ntp.Policy' resource.
        resp_ntp_policy = api_instance.create_ntp_policy(ntp_policy)
        pprint(resp_ntp_policy)
        return resp_ntp_policy
    except intersight.ApiException as e:
        print("Exception when calling NtpApi->create_ntp_policy: %s\n" % e)
        sys.exit(1)


def create_smtp_policy():
    # Create an instance of the API class
    api_instance = smtp_api.SmtpApi(api_client)

    # Create an instance of organization.
    organization = create_organization()

    # SmtpPolicy | The 'smtp.Policy' resource to create.
    smtp_policy = SmtpPolicy()

    # Setting all the attributes for server_profile instance.
    smtp_policy.name = "sample_smtp_policy1"
    smtp_policy.description = "sample smtp policy."
    smtp_policy.enabled = True
    smtp_policy.min_severity = "critical"
    smtp_policy.smtp_recipients = ["test@test"]
    smtp_policy.smtp_server = "10.10.10.80"
    smtp_policy.organization = organization

    # example passing only required values which don't have defaults set
    try:
        # Create a 'smtp.Policy' resource.
        resp_smtp_policy = api_instance.create_smtp_policy(smtp_policy)
        pprint(resp_smtp_policy)
        return resp_smtp_policy
    except intersight.ApiException as e:
        print("Exception when calling SmtpApi->create_smtp_policy: %s\n" % e)
        sys.exit(1)


def create_snmp_policy():
    # Create an instance of the API class
    api_instance = snmp_api.SnmpApi(api_client)

    # Create an instance of organization.
    organization = create_organization()

    # SmtpPolicy | The 'smtp.Policy' resource to create.
    snmp_policy = SnmpPolicy()

    # Setting all the attributes for server_profile instance.
    snmp_policy.name = "sample_snmp_policy1"
    snmp_policy.description = "sample snmp policy."
    snmp_policy.enabled = True
    snmp_policy.sys_location = "BLR"
    snmp_policy.trap_community = "snmpv3"
    snmp_policy.engine_id = "12121"
    snmp_policy.snmp_port = 161
    snmp_policy.sys_contact = "DA"
    snmp_user = SnmpUser(class_id="snmp.User",
                         object_type="snmp.User",
                         auth_type="SHA",
                         privacy_type="AES",
                         security_level="AuthPriv",
                         name="user1",
                         auth_password="Auth_Snmp_user1",
                         privacy_password="Priv_Snmp_user1",
                         )
    snmp_policy.snmp_users = [snmp_user]
    snmp_policy.organization = organization

    # example passing only required values which don't have defaults set
    try:
        # Create a 'Snmp.Policy' resource.
        resp_snmp_policy = api_instance.create_snmp_policy(snmp_policy)
        pprint(resp_snmp_policy)
        return resp_snmp_policy
    except intersight.ApiException as e:
        print("Exception when calling SnmpApi->create_snmp_policy: %s\n" % e)
        sys.exit(1)


def attach_server_to_profile(server_profile_moid):
    api_instance = server_api.ServerApi(api_client)

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

    # Creation of server profile model instance.
    server_profile = ServerProfile()

    # Creation of compute physical relationship object.
    # This instance contains moid of chosen rack unit.
    assigned_server = ComputePhysicalRelationship(class_id="mo.MoRef",
                                                  object_type="compute.RackUnit",
                                                  moid=rack_unit_moid)

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

# create a server profile
server_profile_response = create_server_profile()

# Finding out server profile moid
server_profile_moid = server_profile_response.moid

# create a couple of server policies

# Creating NTP policy
ntp_policy_response = create_ntp_policy()

# Creating SMTP policy
smtp_policy_response = create_smtp_policy()

# Creating SNMP policy
snmp_policy_response = create_snmp_policy()

# Creating a policy mapping with object Type as key and moid will be value.
policies = {
    "ntp.Policy": ntp_policy_response.moid,
    "smtp.Policy": smtp_policy_response.moid,
    "snmp.Policy": snmp_policy_response.moid,
}

# attach the profile to policies
attach_policies_to_profile(policies, server_profile_moid)

# assign a server to the server profile
attach_server_to_profile(server_profile_moid)

# trigger deployment of the server profile
deploy_server_profile(server_profile_moid)
