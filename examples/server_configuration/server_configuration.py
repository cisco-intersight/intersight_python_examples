from examples.authentication import client
from intersight.model.server_profile import ServerProfile
from intersight.api import server_api
from intersight.model.policy_abstract_config_profile_relationship import PolicyAbstractConfigProfileRelationship
from intersight.model.ntp_policy import NtpPolicy
from intersight.api import ntp_api
from intersight.model.smtp_policy import SmtpPolicy
from intersight.api import smtp_api
from intersight.model.snmp_policy import SnmpPolicy
from intersight.api import snmp_api
from intersight.model.snmp_user import SnmpUser
from intersight.model.organization_organization_relationship import OrganizationOrganizationRelationship
from pprint import pprint
import intersight
import sys

api_key = "api_key"
api_key_file = "~/api_key_file_path"

api_client = client.get_api_client(api_key, api_key_file)


def create_organization():
    # Creating an instance of organization
    organization = OrganizationOrganizationRelationship(class_id="mo.MoRef",
                                                        object_type="organization.Organization")

    return organization


def create_profile(server_profile_moid):
    profile = PolicyAbstractConfigProfileRelationship(moid=server_profile_moid,
                                                      object_type="server.Profile",
                                                      class_id="mo.MoRef")
    return profile


def create_server_profile():
    api_instance = server_api.ServerApi(api_client)

    # Create an instance of organization.
    organization = create_organization()

    # ServerProfile | The 'server.Profile' resource to create.
    server_profile = ServerProfile()

    # Setting all the attributes for server_profile instance.
    server_profile.set_attribute("name", "sample_server_profile1")
    server_profile.set_attribute("description", "sample server profile.")
    server_profile.set_attribute("organization", organization)

    # example passing only required values which don't have defaults set
    try:
        # Create a 'server.Profile' resource.
        api_response = api_instance.create_server_profile(server_profile)
        pprint(api_response)
        return api_response
    except intersight.ApiException as e:
        print("Exception when calling ServerApi->create_server_profile: %s\n" % e)
        sys.exit(1)


def create_ntp_policy(server_profile_moid):
    api_instance = ntp_api.NtpApi(api_client)

    # Create an instance of organization.
    organization = create_organization()

    # NtpPolicy | The 'ntp.Policy' resource to create.
    ntp_policy = NtpPolicy()

    # Setting all the attributes for server_profile instance.
    ntp_policy.set_attribute("name", "sample_ntp_policy1")
    ntp_policy.set_attribute("description", "sample ntp policy.")
    ntp_policy.set_attribute("organization", organization)
    ntp_servers = [
       "10.10.10.250", "10.10.10.10", "10.10.10.20", "10.10.10.30"
    ]
    ntp_policy.set_attribute("ntp_servers", ntp_servers)
    profile = create_profile(server_profile_moid)
    ntp_policy.set_attribute("profiles", [profile])

    # example passing only required values which don't have defaults set
    try:
        # Create a 'ntp.Policy' resource.
        api_response = api_instance.create_ntp_policy(ntp_policy)
        pprint(api_response)
        return api_response
    except intersight.ApiException as e:
        print("Exception when calling NtpApi->create_ntp_policy: %s\n" % e)
        sys.exit(1)


def create_smtp_policy(server_profile_moid):
    # Create an instance of the API class
    api_instance = smtp_api.SmtpApi(api_client)

    # Create an instance of organization.
    organization = create_organization()

    # SmtpPolicy | The 'smtp.Policy' resource to create.
    smtp_policy = SmtpPolicy()

    # Setting all the attributes for server_profile instance.
    smtp_policy.set_attribute("name", "sample_smtp_policy1")
    smtp_policy.set_attribute("description", "sample smtp policy.")
    smtp_policy.set_attribute("enabled", True)
    smtp_policy.set_attribute("min_severity", "critical")
    smtp_policy.set_attribute("smtp_recipients", ["test@test"])
    smtp_policy.set_attribute("smtp_server", "10.10.10.80")
    smtp_policy.set_attribute("organization", organization)
    profile = create_profile(server_profile_moid)
    smtp_policy.set_attribute("profiles", [profile])

    # example passing only required values which don't have defaults set
    try:
        # Create a 'smtp.Policy' resource.
        api_response = api_instance.create_smtp_policy(smtp_policy)
        pprint(api_response)
        return api_response
    except intersight.ApiException as e:
        print("Exception when calling SmtpApi->create_smtp_policy: %s\n" % e)
        sys.exit(1)


def create_snmp_policy(server_profile_moid):
    # Create an instance of the API class
    api_instance = snmp_api.SnmpApi(api_client)

    # Create an instance of organization.
    organization = create_organization()

    # SmtpPolicy | The 'smtp.Policy' resource to create.
    snmp_policy = SnmpPolicy()

    # Setting all the attributes for server_profile instance.
    snmp_policy.set_attribute("name", "sample_snmp_policy1")
    snmp_policy.set_attribute("description", "sample snmp policy.")
    snmp_policy.set_attribute("enabled", True)
    snmp_policy.set_attribute("sys_location", "BLR")
    snmp_policy.set_attribute("trap_community", "snmpv3")
    snmp_policy.set_attribute("engine_id", "12121")
    snmp_policy.set_attribute("snmp_port", 161)
    snmp_policy.set_attribute("sys_contact", "DA")
    snmp_user = SnmpUser(class_id="snmp.User",
                         object_type="snmp.User",
                         auth_type="SHA",
                         privacy_type="AES",
                         security_level="AuthPriv",
                         name="user1",
                         auth_password="Auth_Snmp_user1",
                         privacy_password="Priv_Snmp_user1",
                         )
    snmp_policy.set_attribute("snmp_users", [snmp_user])
    snmp_policy.set_attribute("organization", organization)
    profile = create_profile(server_profile_moid)
    snmp_policy.set_attribute("profiles", [profile])

    # example passing only required values which don't have defaults set
    try:
        # Create a 'smtp.Policy' resource.
        api_response = api_instance.create_snmp_policy(snmp_policy)
        pprint(api_response)
        return api_response
    except intersight.ApiException as e:
        print("Exception when calling SmtpApi->create_smtp_policy: %s\n" % e)
        sys.exit(1)


# create a server profile
server_profile_response = create_server_profile()

# Finding out server profile moid
server_profile_moid = server_profile_response.moid

# create a couple of server policies and attach the profile to the policies.

# Creating NTP policy
ntp_policy_response = create_ntp_policy(server_profile_moid)

# Creating SMTP policy
smtp_policy_response = create_smtp_policy(server_profile_moid)

# Creating SNMP policy
snmp_policy_response = create_snmp_policy(server_profile_moid)

# assign a server to the server profile

# trigger deployment of the server profile