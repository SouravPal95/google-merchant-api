# Description:

A stateless rest API for interacting with a google merchant account using OAuth Authentication. 

# Environment setup:

Run the following piece of code in a bash shell:

```bash
$ git clone git@github.com:SouravPal95/google-merchant-api.git
$ cd google-merchant-api
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

It is crucial to generate fresh oAuth2 credentials for `"App-Type":"Web-Application"` from google api console. The generated credentials are downloaded as  `client_secrets_web.json`.

# Making the api calls:

There are three resources namely:
```
Authorize
ListProducts
Products
```
At first, a `GET` request to the `Authorize` resource is made to initiate OAuth2.0 and acquire access and refresh tokens which are programmatically stored in a sql/nosql database. A postman collection has been included in the repository named `google content api.postman_collection.json`.
