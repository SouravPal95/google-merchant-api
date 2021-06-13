# Description:

A stateless rest API for interacting with a google merchant account using OAuth.

# Environment setup.

Run the following piece of code in a bash shell:

```bash
$ pip install virtualenv
$ virtualenv <Name>
$ source <Name>/Script/activate
$ pip install -r requirements.txt
```
# Running local server:

```
$ flask run
```

# Making the api calls:

There are three resources namely:
```
Authorize
ListProducts
Products
```
At first, a get request to the `Authorize` resource is made to acquire access and refresh tokens along with other credentials in JSON format. For every other request to the remaining two resources, this credential is be passed on in the header.
