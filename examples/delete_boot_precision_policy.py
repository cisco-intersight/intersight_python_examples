from examples.authentication import client
from intersight.api import boot_api
from intersight.exceptions import NotFoundException
from pprint import pprint
import intersight

api_key = "api_key"
api_key_file = "~/api_key_file_path"

api_client = client.get_api_client(api_key, api_key_file)

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

# Enter a context with an instance of the API client
with api_client:
    # Create an instance of the API class
    api_instance = boot_api.BootApi(api_client)

    # Getting the response for existing object.
    response = get_boot_precision_policy(api_client)

    # Handling error scenario if get_boot_precision_policy does not return any entry.
    if not response.results:
        raise NotFoundException(reason="The response does not contain any entry for boot precision policy. "
                                       "Please create a boot precision policy and then delete it.")

    # Fetching the moid from the Result's first entry.
    moid = response.results[0].moid

    # example passing only required values which don't have defaults set
    try:
        # Delete a 'boot.PrecisionPolicy' resource.
        api_instance.delete_boot_precision_policy(moid)
        print(f"Deletion for moid: %s was successful"%moid)
    except intersight.ApiException as e:
        print("Exception when calling BootApi->delete_boot_precision_policy: %s\n" % e)
