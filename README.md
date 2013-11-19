pyscrive
========

Python integration for scrive.com

usage:
```python
from pyscrive import Scrive

# I got this ID from the URL when creating template on Scrive.com
MY_TEMPLATE_ID = '93234923421364'

# You need to get these from https://scrive.com/account#api-dashboard
OAUTH_CONSUMER_KEY          = '1'  # Client credentials identifier
OAUTH_TOKEN                 = '2'  # Token credentials identifier
OAUTH_SIGNATURE             = "3&4" # Client credentials secret&Token credentials secret

# Init Sctive
scrive = Scrive()

# create new document from template.
resp_json = scrive.create_document(MY_TEMPLATE_ID)

# all the data of your customer
customers_data = {
    'name': 'John Doe',
    'email': 'john.doe@example.com',
    # add here all the fields of your document.
}

# update document with customer's data
resp_json = scrive.update_document(resp_json, customers_data)

# prepare document for signing
ready     = scrive.ready_document(resp_json)

# sign it yourself
signed    = scrive.sign_document(resp_json)

# now customer got his copy of the document by email and we are waiting for his signature.
```
