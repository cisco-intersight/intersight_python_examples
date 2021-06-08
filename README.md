## Table of Contents
1. [ Authentication ](#authentication)
2. [ Creating an Object ](#creating-an-object)
3. [ Creating an Object from JSON ](#creating-an-object-from-json)
4. [ Reading an Object ](#reading-an-object)
5. [ Updating an Object ](#updating-an-object)
6. [ Deleting an Object ](#deleting-an-object)
7. [ Triggering a Workflow ](#triggering-a-workflow)
8. [ Monitoring a Workflow ](#monitoring-a-workflow)
9. [ Debugging ](#debugging)







<a name="authentication"></a>
## 1. Authentication

- Start with creating an API Client object by specifying an API Key and an API Secret file path.
- This method also specifies which endpoint will the client connect to.
- There is no explicit login when using API Client and Secret. Every message carries the information required for authentication.

```python
import intersight
import re


def get_api_client(api_key_id, api_secret_file, endpoint="https://intersight.com"):
    with open(api_secret_file, 'r') as f:
        api_key = f.read()

    if re.search('BEGIN RSA PRIVATE KEY', api_key):
        # API Key v2 format
        signing_algorithm = intersight.signing.ALGORITHM_RSASSA_PKCS1v15
        signing_scheme = intersight.signing.SCHEME_RSA_SHA256
        hash_algorithm = intersight.signing.HASH_SHA256

    elif re.search('BEGIN EC PRIVATE KEY', api_key):
        # API Key v3 format
        signing_algorithm = intersight.signing.ALGORITHM_ECDSA_MODE_DETERMINISTIC_RFC6979
        signing_scheme = intersight.signing.SCHEME_HS2019
        hash_algorithm = intersight.signing.HASH_SHA256

    configuration = intersight.Configuration(
        host=endpoint,
        signing_info=intersight.signing.HttpSigningConfiguration(
            key_id=api_key_id,
            private_key_path=api_secret_file,
            signing_scheme=signing_scheme,
            signing_algorithm=signing_algorithm,
            hash_algorithm=hash_algorithm,
            signed_headers=[
                intersight.signing.HEADER_REQUEST_TARGET,
                intersight.signing.HEADER_HOST,
                intersight.signing.HEADER_DATE,
                intersight.signing.HEADER_DIGEST,
            ]
        )
    )

    return intersight.ApiClient(configuration)
```

Once an API Client is created, it can be used to communicate with the Intersight server.
```python

from intersight.api import boot_api
from intersight.model.boot_precision_policy import BootPrecisionPolicy


api_client = get_api_client("api_key", "~/api_secret_file_path")

# Create an api instance of the correct API type
api_instance = boot_api.BootApi(api_client)

# Create an object locally and populate the object properties
boot_precision_policy = BootPrecisionPolicy()


# Create an object in Intersight
api_response = api_instance.create_boot_precision_policy(boot_precision_policy)    
```


<a name="creating-an-object"></a>
## 2. Creating an Object

<a name="creating-an-object-from-json"></a>
## 3. Creating an Object from JSON

<a name="reading-an-object"></a>
## 4. Reading an Object

<a name="updating-an-object"></a>
## 5. Updating an Object

<a name="deleting-an-object"></a>
## 6. Deleting an Object

<a name="triggering-a-workflow"></a>
## 7. Triggering a Workflow

<a name="monitoring-a-workflow"></a>
## 8. Monitoring a Workflow

<a name="debugging"></a>
## 8. Debugging


