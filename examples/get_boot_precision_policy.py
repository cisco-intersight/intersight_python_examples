from examples.authentication import client
from intersight.api import boot_api
from pprint import pprint
import intersight

api_key = "api_key"
api_key_file = "~/api_key_file_path"

api_client = client.get_api_client(api_key, api_key_file)

# Enter a context with an instance of the API client
with api_client:
    # Create an instance of the API class
    api_instance = boot_api.BootApi(api_client)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Read a 'boot.PrecisionPolicy' resource.
        api_response = api_instance.get_boot_precision_policy_list()
        pprint(api_response)
    except intersight.ApiException as e:
        print("Exception when calling BootApi->get_boot_precision_policy_list: %s\n" % e)
