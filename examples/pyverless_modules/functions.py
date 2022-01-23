from pprint import pprint

from framework import framework
from pyverless import Function, FunctionEvent, EventTypes


class ShortFunction(Function):
    def __init__(self, sls_framework, name, handler, **kwargs):
        kwargs["timeout"] = 5
        super().__init__(sls_framework, name, handler, **kwargs)


class LongFunction(Function):
    def __init__(self, sls_framework, name, handler, **kwargs):
        kwargs["timeout"] = 30
        super().__init__(sls_framework, name, handler, **kwargs)


class ApiFunction(Function):
    def __init__(self, sls_framework, name, handler, path, method, **kwargs):
        kwargs["events"] = [
            FunctionEvent(
                EventTypes.httpApi, path=path, method=method
            )
        ]
        super().__init__(sls_framework, name, handler, **kwargs)


class SnsFunction(Function):
    def __init__(self, sls_framework, name, handler, topic_arn, **kwargs):
        kwargs["events"] = [
            FunctionEvent(
                EventTypes.SNS, topic_arn
            )
        ]
        super().__init__(sls_framework, name, handler, **kwargs)


SnsFunction(framework, "sns_function", "sns_function.handler", "arn:aws:sns:us-east-1:123456789012:my-topic")


if __name__ == "__main__":
    pprint(framework.__dict__())
