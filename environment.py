from reusables.swagger_base import SwaggerClientBase

def before_all(context):
    # Access userdata
    swagger_url = context.config.userdata.get("swagger_url")    
    print(f"Swagger URL: {swagger_url}")
    context.swagger_url=swagger_url

def before_scenario(context,scenario):
    client = SwaggerClientBase(context.swagger_url)
    context.client=client