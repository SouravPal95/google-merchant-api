# Description:

A stateless rest API for interacting with a google merchant account using OAuth Authentication. 

# Environment setup:

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

# Generating Credentials:

It is crucial to generate fresh oAuth2 credentials for desktop or webapp from google api console. The generated credentials download the credentials as `client_secrets_desk.json` or  `client_secrets_web.json` based on the app type.

# Making the api calls:

There are three resources namely:
```
Authorize
ListProducts
Products
```
At first, a get request to the `Authorize` resource is made to acquire access and refresh tokens along with other credentials in JSON format. For every other request to the remaining two resources, this credential is be passed on in the header.
