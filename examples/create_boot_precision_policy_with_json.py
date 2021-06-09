from examples.authentication import client
import json
from intersight.api import boot_api
from intersight.model.boot_precision_policy import BootPrecisionPolicy
from intersight.model.boot_device_base import BootDeviceBase
from intersight.model.organization_organization_relationship import OrganizationOrganizationRelationship
from pprint import pprint
import intersight

api_key = "api_key"
api_key_file = "~/api_key_file_path"

api_client = client.get_api_client(api_key, api_key_file)

# Enter a context with an instance of the API client.
with api_client:
    # Create an instance of the API class.
    api_instance = boot_api.BootApi(api_client)

    data_json_file_path = "data.json"
    with open(data_json_file_path, "r") as json_data_file:
        json_data = json_data_file.read()

    # Loading the json objects into python dictionary.
    data = json.loads(json_data)

    # BootPrecisionPolicy | The 'boot.PrecisionPolicy' resource to create.
    boot_precision_policy = BootPrecisionPolicy(**data, _spec_property_naming=True,
                                                _configuration=api_client.configuration)

    # example passing only required values which don't have defaults set
    try:
        # Create a 'boot.PrecisionPolicy' resource.
        api_response = api_instance.create_boot_precision_policy(boot_precision_policy)
        pprint(api_response)
    except intersight.ApiException as e:
        print("Exception when calling BootApi->create_boot_precision_policy: %s\n" % e)
