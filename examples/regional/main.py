from pyverless import ServerlessFramework, Provider, Function, Constants, RegionalParam, StageRegionParam

sls = ServerlessFramework(
    framework_version="2.70.0",
    service="ras",
    provider=Provider(
        name='aws',
        runtime='python3.8',
        lambda_hashing_version='20201221',
    )
)

regional_timeout = RegionalParam(
    sls_framework=sls,
    name="api_timeout",
    mapping={
        "us-east-1": 10,
        "us-east-2": 20
    },
    default=30
)

stage_region_name = StageRegionParam(
    sls_framework=sls,
    name="memory_size",
    mapping={
        ("dev", "us-east-1"): 128,
        ("prod", "us-east-1"): 1024,
        ("prod", "eu-west-1"): 512,
    },
    default=256
)

Function(
    sls,
    "api",
    handler="api.handler",
    timeout=regional_timeout.key,
    memory_size=stage_region_name.key,
    environment={
        "AWS_REGION": Constants.REGION,
        "STAGE": Constants.STAGE,
    }
)
