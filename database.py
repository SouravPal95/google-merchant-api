from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine=create_engine(r"sqlite:///D:\Abstract Inc (Filed)\google-api\data.db", 
                     connect_args={'check_same_thread': False},
                     echo=True)

Base=declarative_base(bind=engine)

Session=sessionmaker(bind=engine)
session=Session()

class Credential(Base):
    __tablename__="credentials"
    id=Column(Integer, primary_key=True)
    merchant_id=Column(Integer, nullable=False)
    token=Column(String)
    refresh_token=Column(String)
    
    def generate_credentials(self):
        return {
            'token': self.token,
            'refresh_token': self.refresh_token,
            'token_uri': "https://oauth2.googleapis.com/token",
            'client_id': "1092016066629-r8maka40hpbpelillfnoiq8r997ot2o7.apps.googleusercontent.com",
            'client_secret': "nAadNvVsVH-NvwFMguWbzz-I",
            'scopes': [
                "https://www.googleapis.com/auth/content"
            ]
        }
    
    def __repr__(self):
        return f"Credential<merchant_id:{self.merchant_id}>"