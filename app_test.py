import json
from googleapiclient.discovery import build
from authentication import credentials


with build("content", "v2.1",
              credentials=credentials) as service:

    print(f'service: {service}')

    products=service.products()

    print(f'products: {products}')

    request=products.list(merchantId=433480089)

    print(f'request: {request}')

    response=request.execute()
    

    print(f'Response: {response}')

