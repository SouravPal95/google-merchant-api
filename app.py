
from itertools import product
from google.oauth2 import credentials

from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from flask import Flask, redirect, url_for, session, jsonify
from flask.globals import request
from flask_restful import Resource, Api
#from flask_cors import CORS

app=Flask(__name__)
#cors=CORS(app)
api=Api(app)

app.config['SECRET_KEY']="23e01632e0d475932a8ecc3b1177bc574f9e0adbb9efd19f76f76b4faa860f20"

class Authorize(Resource):
    def get(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets_desk.json',
            scopes=['https://www.googleapis.com/auth/content']
        )
        credentials=flow.run_local_server(host='localhost',
                        port=8080,
                        authorization_prompt_message='Please visit this URL: {url}', 
                        success_message='The auth flow is complete; you may close this window.',
                        open_browser=True)
        credentials={
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
            }
        
        return credentials


class ListProducts(Resource):
    def get(self, merch_id=433480089):

        headers = request.headers
        if not headers.get("Refresh_Token"):
            return {
                'message': 'Unauthorized',
            }
        credentials = {
            'token': headers.get('Token', None),
            'refresh_token': headers.get('Refresh_Token', None),
            'token_uri': headers.get('Token_Uri', None),
            'client_id': headers.get('Client_Id', None),
            'client_secret': headers.get('Client_Secret', None),
            'scopes': headers.get('Scopes', None).split(" ")
        }
           
        credentials=Credentials(**credentials)
        service=build('content', 'v2.1',
                      credentials=credentials)
        products=service.products()
        request_=products.list(merchantId=merch_id)
        response=request_.execute()
        service.close()
        
        return jsonify(response)

class Product(Resource):
    def get(self, merch_id):
        headers = request.headers
        if not headers.get("Refresh_Token"):
            return {
                'message': 'Unauthorized',
            }
        credentials = {
            'token': headers.get('Token', None),
            'refresh_token': headers.get('Refresh_Token', None),
            'token_uri': headers.get('Token_Uri', None),
            'client_id': headers.get('Client_Id', None),
            'client_secret': headers.get('Client_Secret', None),
            'scopes': headers.get('Scopes', None).split(" ")
        }
           
        credentials=Credentials(**credentials)
        with build('content', 'v2.1', credentials=credentials) as service:
            products=service.products()
            request_=products.get(merchantId=merch_id, 
                                  productId=request.args.get('productId'))
            response=request_.execute()
        
        return jsonify(response)    
    
    def post(self, merch_id):
        headers=request.headers
        if not headers.get('Refresh_Token'):
            return {
                "message": "Unauthorized"
            }
        credentials = {
            'token': headers.get('Token', None),
            'refresh_token': headers.get('Refresh_Token', None),
            'token_uri': headers.get('Token_Uri', None),
            'client_id': headers.get('Client_Id', None),
            'client_secret': headers.get('Client_Secret', None),
            'scopes': headers.get('Scopes', None).split(" ")
        }
        credentials=Credentials(**credentials)
        product=request.get_json()
        #product=DUMMY_DATA
        with build('content', 'v2.1', credentials=credentials) as service:
            products=service.products()
            request_=products.insert(merchantId=merch_id, body=product)
            response=request_.execute()
        
        return jsonify(response)
    
    def patch(self, merch_id):
        headers=request.headers
        if not headers.get('Refresh_Token'):
            return {
                "message": "Unauthorized"
            }
        credentials = {
            'token': headers.get('Token', None),
            'refresh_token': headers.get('Refresh_Token', None),
            'token_uri': headers.get('Token_Uri', None),
            'client_id': headers.get('Client_Id', None),
            'client_secret': headers.get('Client_Secret', None),
            'scopes': headers.get('Scopes', None).split(" ")
        }
        credentials=Credentials(**credentials)
        product=request.get_json()
        with build('content', 'v2.1', credentials=credentials) as service:
            products=service.products()
            request_=products.update(merchantId=merch_id, body=product, 
                                     productId=request.args.get('productId'))
            response=request_.execute()
        
        return jsonify(response)   
    
    def delete(self, merch_id):
        headers = request.headers
        if not headers.get("Refresh_Token"):
            return {
                'message': 'Unauthorized',
            }
        credentials = {
            'token': headers.get('Token', None),
            'refresh_token': headers.get('Refresh_Token', None),
            'token_uri': headers.get('Token_Uri', None),
            'client_id': headers.get('Client_Id', None),
            'client_secret': headers.get('Client_Secret', None),
            'scopes': headers.get('Scopes', None).split(" ")
        }
           
        credentials=Credentials(**credentials)
        with build('content', 'v2.1', credentials=credentials) as service:
            products=service.products()
            request_=products.delete(merchantId=merch_id, 
                                     productId=request.args.get('productId'))
            response=request_.execute()
        
        return jsonify(response) 

@app.route('/')
def index():
    return jsonify({
        "Message":"Welcome to my demo"
    })


    
@app.route('/authorize2')
def authorize2():
    
    flow = Flow.from_client_secrets_file(
        'client_secrets_web.json',
        scopes=['https://www.googleapis.com/auth/content'],
        redirect_uri=url_for('oauth2callback', 
                             _external=True)
    )
    authorization_url, state=flow.authorization_url(
        access_type="offline",
        include_granted_scopes='true'
    )
    
    session['state']=state
    print(f"state from authorize: {session['state']}")
    return {'url':authorization_url,
            'state':session['state']}
    #return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    
    state=session['state']
    #state=request.headers.get('state')
    print(f'state from callback: {state}')
    flow=Flow.from_client_secrets_file(
        'client_secrets_web.json',
        scopes=['https://www.googleapis.com/auth/content'],
        state=state,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    authorization_resp=request.url
    flow.fetch_token(authorization_response=authorization_resp)
    credentials = {
        'token': flow.credentials.token,
        'refresh_token': flow.credentials.refresh_token,
        'token_uri': flow.credentials.token_uri,
        'client_id': flow.credentials.client_id,
        'client_secret': flow.credentials.client_secret,
        'scopes': flow.credentials.scopes
    }
    session['credentials']=credentials
      
    #return redirect(url_for('index'))
    #return redirect(url_for('products', merch_id=session['merch_id']))
    #return redirect(api.url_for(Products, merch_id=session['merch_id']))
    
    return redirect(session.get('original_url') or url_for('index'))

api.add_resource(ListProducts, '/shop/listproducts', '/shop/<int:merch_id>/listproducts')
api.add_resource(Product, '/shop/<int:merch_id>/product')
api.add_resource(Authorize, '/authorize')

if __name__=="__main__":
    app.run()
    