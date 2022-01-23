import abc
from collections import OrderedDict
from enum import Enum
from functools import reduce
from typing import List, Dict, Optional, Any, Tuple

import yaml


def dict_merge(objects: List['ServerlessObject']):
    d = {}
    for obj in objects:
        d.update(obj.__dict__())
    return d


def remove_non_values(d):
    """
    Removes all keys that are not values from a dictionary.
    """
    return {k: v for k, v in d.items() if v is not None}


class Constants:
    REGION = "${opt:region}"
    STAGE = "${opt:stage}"


class EventTypes(str, Enum):
    http = "http"
    httpApi = "httpApi"
    ALB = "alb"
    SNS = "sns"
    SQS = "sqs"


class ResourceType(str, Enum):
    RESOURCES = "Resources"
    EXTENSIONS = "extensions"
    OUTPUTS = "Outputs"
    CONDITIONS = "Conditions"


def capitalize_str(s: str, with_first=False):
    if not isinstance(s, str):
        return s
    first_word, *words = s.split("_")
    first_word = first_word.capitalize() if with_first else first_word
    capitalized = "".join([first_word] + [k.capitalize() for k in words])
    return capitalized


def convert_snake_keys_to_capitalize(dictionary):
    """
    Converts all keys in a dictionary to capitalized keys.
    """
    return {capitalize_str(k): v for k, v in dictionary.items()}


class SlsSerialize:
    @classmethod
    def __sorter(cls, k):
        starters, enders = getattr(cls, "__sort_order__", ([], []))
        if k[0] in starters:
            return -1
        if k[0] in enders:
            return 1
        return 0

    def __dict__(self):
        name = getattr(self, '_object_name', None)
        d = getattr(self, '_d', {})
        d = convert_snake_keys_to_capitalize(d)
        d = OrderedDict(sorted(d.items(), key=self.__sorter))
        return {name: d} if name else d


class ServerlessObject(SlsSerialize):
    def __init__(self, sls_framework: 'ServerlessFramework' = None, resource_name: Optional[str] = None, **kwargs):
        self._d = kwargs
        self._object_name = resource_name
        if sls_framework:
            sls_framework.register_resource(self)

    @classmethod
    def resource_type(cls):
        raise NotImplementedError()


class ServerlessFramework(SlsSerialize):
    __sort_order__ = ["service", "frameworkVersion", "disabledDeprecations", "provider", "plugins", "custom"], [
        "resources"]

    def __init__(self, framework_version: str, service: str, provider: 'Provider' = None, **kwargs):
        self._framework_version = framework_version
        self._service = service
        if "custom" not in kwargs:
            kwargs["custom"] = {}
        self._extra_args = kwargs
        self._provider = provider
        self._resources = []
        self._functions = []
        self._package = []

    @property
    def _d(self):
        return remove_non_values(convert_snake_keys_to_capitalize(dict(
            framework_version=self._framework_version,
            service=self._service,
            provider=self._provider.__dict__(),
            resources=[resource.__dict__() for resource in self._resources] if self._resources else None,
            functions=dict_merge(self._functions),
            package=dict_merge(self._package),
            **self._extra_args
        )))

    def register_resource(self, sls_object: ServerlessObject):
        if not isinstance(sls_object, ServerlessObject):
            raise Exception('Invalid object type')
        elif sls_object.resource_type() == "Function":
            self._functions.append(sls_object)
        elif sls_object.resource_type() == "Resource":
            self._resources.append(sls_object)
        elif sls_object.resource_type() == "Package":
            self._package.append(sls_object)
        elif sls_object.resource_type() == "Provider":
            assert self._provider is None, "Only one provider is allowed"
            self._provider = sls_object

    @property
    def custom(self):
        return self._extra_args.get("custom")

    @custom.setter
    def custom(self, value):
        self._extra_args["custom"] = value

    @property
    def plugins(self):
        return self._extra_args.get("plugins")

    @plugins.setter
    def plugins(self, value):
        self._extra_args["plugins"] = value

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, value):
        self._provider = value


class Function(ServerlessObject):
    __sort_order__ = ["handler", "image", "name"], ["events", "environment"]

    def __init__(self, sls_framework: 'ServerlessFramework', name: str, handler: str, image: str = None,
                 architecture: str = None, override_name: str = None, description: str = None,
                 memory_size: int = None, reserved_concurrency: int = None, provisioned_concurrency: int = None,
                 runtime: str = None, timeout: int = None, role: str = None, on_error: str = None,
                 kms_key_arn: str = None, disable_logs: bool = None, environment: Dict[str, str] = None,
                 tags: Dict[str, str] = None, vpc: Dict[str, Any] = None, layers: List[str] = None, tracing: str = None,
                 condition: str = None, depends_on: List[str] = None, destinations: Dict = None,
                 file_system_config: Dict = None, events: List['FunctionEvent'] = None):
        super().__init__(sls_framework, name, **remove_non_values(dict(
            handler=handler,
            image=image,
            architecture=architecture,
            override_name=override_name,
            description=description,
            memory_size=memory_size,
            reserved_concurrency=reserved_concurrency,
            provisioned_concurrency=provisioned_concurrency,
            runtime=runtime,
            timeout=timeout,
            role=role,
            on_error=on_error,
            kms_key_arn=kms_key_arn,
            disable_logs=disable_logs,
            environment=environment,
            tags=tags,
            vpc=vpc,
            layers=layers,
            tracing=tracing,
            condition=condition,
            depends_on=depends_on,
            destinations=destinations,
            file_system_config=file_system_config,
            events=events
        )))

    @classmethod
    def resource_type(cls):
        return 'Function'

    def __dict__(self):
        s_dict = super().__dict__()
        s_def = s_dict[list(s_dict.keys())[0]]
        if "events" in s_def:
            s_def["events"] = [event.__dict__() for event in s_def["events"]]
        return {self._object_name: s_def}


class FunctionEvent:
    def __init__(self, event_type: EventTypes, *args, **kwargs):
        self._event_type = event_type.value
        self._kwargs = kwargs
        self._args = args

    def __dict__(self):
        if self._kwargs:
            return {self._event_type: convert_snake_keys_to_capitalize(self._kwargs)}
        elif len(self._args) == 1:
            return {self._event_type: self._args[0]}
        elif len(self._args) > 1:
            return {self._event_type: self._args}
        else:
            return self._event_type


class Provider(ServerlessObject):
    def __init__(self, sls_framework: 'ServerlessFramework' = None, **kwargs):
        super().__init__(sls_framework, '', **kwargs)

    def resource_type(self):
        return 'Provider'

    def __dict__(self):
        return convert_snake_keys_to_capitalize(self._d)


class ResourceGroup(ServerlessObject):
    def __init__(self, sls_framework: 'ServerlessFramework', name: str,
                 resource_type: ResourceType = ResourceType.RESOURCES,
                 resources: List['Resource'] = None):
        self._resources = resources or []
        self._resource_type = resource_type
        super().__init__(sls_framework, name)

    def resource_type(self):
        return 'Resource'

    def add_resource(self, resource):
        self._resources.append(resource)

    def __dict__(self):
        return {self._resource_type.value: {resource.name: resource.__dict__() for resource in self._resources}}


class Resource:
    def __init__(self, resource_group: 'ResourceGroup', name: str, **kwargs):
        self.name = capitalize_str(name, with_first=True)
        self._extra_args = kwargs
        resource_group.add_resource(self)

    def __dict__(self):
        return {**self._extra_args}


class Package(ServerlessObject):
    def __init__(self, sls_framework: ServerlessFramework, patterns: List[str] = None,
                 exclude_dev_dependencies: bool = None, artifact: str = None,
                 individually: bool = None, exclude: List[str] = None, include: List[str] = None, **kwargs):
        super().__init__(sls_framework, **remove_non_values(dict(
            patterns=patterns,
            exclude_dev_dependencies=exclude_dev_dependencies,
            artifact=artifact,
            individually=individually,
            exclude=exclude,
            include=include,
            **kwargs
        )))

    def resource_type(self):
        return 'Package'


class ParamMeta(abc.ABC):
    param_name = ''

    def __init__(self, sls_framework: ServerlessFramework, name: str, mapping: Dict[str, Any], default: Any):
        self._mapping_key = f"param_{name}_mapping"
        mapping["default"] = default
        sls_framework.custom[self._mapping_key] = mapping

    @property
    def key(self):
        return "${self:custom.%s.%s, self:custom.%s.default}" % (self._mapping_key, self.param_name, self._mapping_key)


class RegionalParam(ParamMeta):
    param_name = Constants.REGION


class StageParam(ParamMeta):
    param_name = Constants.STAGE


class StageRegionParam(ParamMeta):
    param_name = f"{Constants.STAGE}_{Constants.REGION}"

    def __init__(self, sls_framework, name: str, mapping: Dict[Tuple[str, str], Any], default: Any):
        mapping = {f"{k[0]}_{k[1]}": v for k, v in mapping.items()}
        super().__init__(sls_framework, name, mapping, default)
