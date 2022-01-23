from pyverless import ServerlessFramework, Provider

framework = ServerlessFramework(
    framework_version="2.70.0",
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

framework.provider = Provider(
    name='aws',
    runtime='python3.8',
    lambda_hashing_version='20201221',
    iam={
        "role": {
            "statements": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "dynamodb:Query",
                        "dynamodb:Scan",
                        "dynamodb:GetItem",
                        "dynamodb:PutItem",
                        "dynamodb:UpdateItem",
                        "dynamodb:DeleteItem",
                    ],
                    "Resource": "arn:aws:dynamodb:*:*:table/ras-*"
                }
            ]
        }
    }
)
