from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from flask import Flask, url_for, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS

from database import Session, Credential

app=Flask(__name__)

app.config['SECRET_KEY']="23e01632e0d475932a8ecc3b1177bc574f9e0adbb9efd19f76f76b4faa860f20"

cors=CORS(app)
api=Api(app)

session = Session()

class ListProducts(Resource):
    def get(self, merch_id=433480089):
            
        merchant=session.query(Credential).filter(Credential.merchant_id==merch_id).first()
        if not merchant:
            return {
                'message': 'Unauthorized',
            }
        
        credentials = merchant.generate_credentials()
           
        credentials=Credentials(**credentials)
        with build('content', 'v2.1',
                      credentials=credentials) as service:
            products=service.products()
            request_=products.list(merchantId=merch_id)
            response=request_.execute()
        
        return jsonify(response)

class Product(Resource):
    def get(self, merch_id):
        
        merchant=session.query(Credential).filter(Credential.merchant_id==merch_id).first()
        if not merchant:
            return {
                'message': 'Unauthorized',
            }
        
        credentials = merchant.generate_credentials()
           
        credentials=Credentials(**credentials)
        with build('content', 'v2.1', credentials=credentials) as service:
            products=service.products()
            request_=products.get(merchantId=merch_id, 
                                  productId=request.args.get('productId'))
            response=request_.execute()
        
        return jsonify(response)    
    
    def post(self, merch_id):
        merchant=session.query(Credential).filter(Credential.merchant_id==merch_id).first()
        if not merchant:
            return {
                'message': 'Unauthorized',
            }
        
        credentials =  merchant.generate_credentials()
        
        credentials=Credentials(**credentials)
        product=request.get_json()
        with build('content', 'v2.1', credentials=credentials) as service:
            products=service.products()
            request_=products.insert(merchantId=merch_id, body=product)
            response=request_.execute()
        
        return jsonify(response)
    
    def patch(self, merch_id):
        merchant=session.query(Credential).filter(Credential.merchant_id==merch_id).first()
        if not merchant:
            return {
                'message': 'Unauthorized',
            }
        
        credentials = merchant.generate_credentials()
        
        credentials=Credentials(**credentials)
        product=request.get_json()
        with build('content', 'v2.1', credentials=credentials) as service:
            products=service.products()
            request_=products.update(merchantId=merch_id, body=product, 
                                     productId=request.args.get('productId'))
            response=request_.execute()
        
        return jsonify(response)   
    
    def delete(self, merch_id):
        merchant=session.query(Credential).filter(Credential.merchant_id==merch_id).first()
        if not merchant:
            return {
                'message': 'Unauthorized',
            }
        
        credentials = merchant.generate_credentials()
           
        credentials=Credentials(**credentials)
        with build('content', 'v2.1', credentials=credentials) as service:
            products=service.products()
            request_=products.delete(merchantId=merch_id, 
                                     productId=request.args.get('productId'))
            response=request_.execute()
        
        return jsonify(response) 
    
class Authorize(Resource):
    def get(self, merchant_id):
        
        flow = Flow.from_client_secrets_file(
            'client_secrets_web.json',
            scopes=['https://www.googleapis.com/auth/content'],
            redirect_uri=url_for('oauth2callback', 
                                _external=True),
            state=merchant_id
        )
        authorization_url, _=flow.authorization_url(
            access_type="offline",
            include_granted_scopes='true'
        )
        
        merchant=Credential(merchant_id=merchant_id)
        session.add(merchant)
        session.commit() 
        return {
            "Authorization Url": authorization_url
        }

@app.route("/")
def index():
    pass

@app.route('/oauth2callback')
def oauth2callback():
    
    flow=Flow.from_client_secrets_file(
        'client_secrets_web.json',
        scopes=['https://www.googleapis.com/auth/content'],
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    authorization_resp=request.url
    flow.fetch_token(authorization_response=authorization_resp)
    merchant=session.query(Credential).filter(Credential.merchant_id==request.args.get('state')).first()
    merchant.token=flow.credentials.token
    merchant.refresh_token=flow.credentials.refresh_token
    session.commit()
 
    return {
        "Message":f"credentials added to db {request.args.get('state')}"
    }

api.add_resource(ListProducts, '/shop/listproducts', '/shop/<int:merch_id>/listproducts')
api.add_resource(Product, '/shop/<int:merch_id>/product')
api.add_resource(Authorize, '/<int:merchant_id>/authorize')

if __name__=="__main__":
    app.run()
    