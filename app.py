from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from flask import Flask, url_for, session, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app=Flask(__name__)

app.config['SECRET_KEY']="23e01632e0d475932a8ecc3b1177bc574f9e0adbb9efd19f76f76b4faa860f20"
app.config['SQLALCHEMY_DATABASE_URI']=r"sqlite:///D:\Abstract Inc (Filed)\google-api\data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

cors=CORS(app)
api=Api(app)
db=SQLAlchemy(app)

class Credential(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    merchant_id=db.Column(db.Integer, nullable=False)
    token=db.Column(db.String)
    refresh_token=db.Column(db.String)
    
    def __repr__(self):
        return f"Credential<merchant_id:{self.merchant_id}>"

class ListProducts(Resource):
    def get(self, merch_id=433480089):
            
        merchant=Credential.query.filter_by(merchant_id=merch_id).first()
        if not merchant:
            return {
                'message': 'Unauthorized',
            }
        
        credentials = {
            'token': merchant.token,
            'refresh_token': merchant.refresh_token,
            'token_uri': "https://oauth2.googleapis.com/token",
            'client_id': "1092016066629-r8maka40hpbpelillfnoiq8r997ot2o7.apps.googleusercontent.com",
            'client_secret': "nAadNvVsVH-NvwFMguWbzz-I",
            'scopes': [
                "https://www.googleapis.com/auth/content"
            ]
        } 
           
        credentials=Credentials(**credentials)
        with build('content', 'v2.1',
                      credentials=credentials) as service:
            products=service.products()
            request_=products.list(merchantId=merch_id)
            response=request_.execute()
        
        return jsonify(response)

class Product(Resource):
    def get(self, merch_id):
        
        merchant=Credential.query.filter_by(merchant_id=merch_id).first()
        if not merchant:
            return {
                'message': 'Unauthorized',
            }
        
        credentials = {
            'token': merchant.token,
            'refresh_token': merchant.refresh_token,
            'token_uri': "https://oauth2.googleapis.com/token",
            'client_id': "1092016066629-r8maka40hpbpelillfnoiq8r997ot2o7.apps.googleusercontent.com",
            'client_secret': "nAadNvVsVH-NvwFMguWbzz-I",
            'scopes': [
                "https://www.googleapis.com/auth/content"
            ]
        } 
           
        credentials=Credentials(**credentials)
        with build('content', 'v2.1', credentials=credentials) as service:
            products=service.products()
            request_=products.get(merchantId=merch_id, 
                                  productId=request.args.get('productId'))
            response=request_.execute()
        
        return jsonify(response)    
    
    def post(self, merch_id):
        merchant=Credential.query.filter_by(merchant_id=merch_id).first()
        if not merchant:
            return {
                'message': 'Unauthorized',
            }
        
        credentials = {
            'token': merchant.token,
            'refresh_token': merchant.refresh_token,
            'token_uri': "https://oauth2.googleapis.com/token",
            'client_id': "1092016066629-r8maka40hpbpelillfnoiq8r997ot2o7.apps.googleusercontent.com",
            'client_secret': "nAadNvVsVH-NvwFMguWbzz-I",
            'scopes': [
                "https://www.googleapis.com/auth/content"
            ]
        } 
        credentials=Credentials(**credentials)
        product=request.get_json()
        with build('content', 'v2.1', credentials=credentials) as service:
            products=service.products()
            request_=products.insert(merchantId=merch_id, body=product)
            response=request_.execute()
        
        return jsonify(response)
    
    def patch(self, merch_id):
        merchant=Credential.query.filter_by(merchant_id=merch_id).first()
        if not merchant:
            return {
                'message': 'Unauthorized',
            }
        
        credentials = {
            'token': merchant.token,
            'refresh_token': merchant.refresh_token,
            'token_uri': "https://oauth2.googleapis.com/token",
            'client_id': "1092016066629-r8maka40hpbpelillfnoiq8r997ot2o7.apps.googleusercontent.com",
            'client_secret': "nAadNvVsVH-NvwFMguWbzz-I",
            'scopes': [
                "https://www.googleapis.com/auth/content"
            ]
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
        merchant=Credential.query.filter_by(merchant_id=merch_id).first()
        if not merchant:
            return {
                'message': 'Unauthorized',
            }
        
        credentials = {
            'token': merchant.token,
            'refresh_token': merchant.refresh_token,
            'token_uri': "https://oauth2.googleapis.com/token",
            'client_id': "1092016066629-r8maka40hpbpelillfnoiq8r997ot2o7.apps.googleusercontent.com",
            'client_secret': "nAadNvVsVH-NvwFMguWbzz-I",
            'scopes': [
                "https://www.googleapis.com/auth/content"
            ]
        } 
           
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
        authorization_url, state=flow.authorization_url(
            access_type="offline",
            include_granted_scopes='true'
        )
        print(f"state from authorize2: {state}")
        session['state']=state
        
        merchant=Credential(merchant_id=merchant_id)
        db.session.add(merchant)
        db.session.commit() 
        return {
            "Authorization Url": authorization_url
        }

@app.route('/oauth2callback')
def oauth2callback():
    
    flow=Flow.from_client_secrets_file(
        'client_secrets_web.json',
        scopes=['https://www.googleapis.com/auth/content'],
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    authorization_resp=request.url
    flow.fetch_token(authorization_response=authorization_resp)
    
    merchant=Credential.query.filter_by(merchant_id=request.args.get('state')).first()
    merchant.token=flow.credentials.token
    merchant.refresh_token=flow.credentials.refresh_token
    db.session.commit()
 
    return {
        "Message":f"credentials added to db {request.args.get('state')}"
    }

api.add_resource(ListProducts, '/shop/listproducts', '/shop/<int:merch_id>/listproducts')
api.add_resource(Product, '/shop/<int:merch_id>/product')
api.add_resource(Authorize, '/<int:merchant_id>/authorize')

if __name__=="__main__":
    app.run()
    