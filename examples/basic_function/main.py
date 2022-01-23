import json
from pprint import pprint

from pyverless import ServerlessFramework, Provider, Function, FunctionEvent, EventTypes

sls = ServerlessFramework(
    framework_version="~2.0.0",
    service="ras",
    plugins=[
        "serverless-wsgi",
        "serverless-python-requirements",
    ],
    custom={
        "wsgi": {
            "app": "app.app"
        }
    }
)

Provider(
    sls,
    name='aws',
    runtime='python3.8',
    lambda_hashing_version='20201221'
)

Function(
    sls,
    'api',
    handler='wsgi_handler.handler',
    events=[
        FunctionEvent(EventTypes.http, path="/", method="ANY"),
        FunctionEvent(EventTypes.httpApi, path="/{proxy+}", method="ANY"),
    ]
)

