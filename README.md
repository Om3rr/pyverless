### The Idea of `pyverless`

when working with ALOT of different microservices and APIs its quite common that we are starting to COPY-PASTE some code
from one `serverless` file to another. creating this `pyverless` let big organizations to share `modules` in a way that
can be used accross the organizations **AS A CODE**

### Getting Started

```python
#main.py

from pyverless import ServerlessFramework, Provider, Function, FunctionEvent, EventTypes

sls = ServerlessFramework(
    framework_version="2 || 3",
    service="aws-python",
)

Provider(
    sls,
    name="aws",
    runtime="python3.8",
    lambda_hashing_version=20201221
)

Function(
    sls,
    name='hello',
    handler='handler.hello',
)
```

Than run `pyls main:sls` and check the `serverless.yml` that created. it will create [this](https://github.com/serverless/examples/blob/master/aws-python/serverless.yml) example serverless.yml file.
*According to sls fw, package.json is not mendatory so right now pyverless wont maintain a package.json file*

### Key Features:

- **Modules** - A module is a collection of related functionality that can be used in different parts of the
  application.
- **Parameters** - A parameter is a value that can be used to configure any part of the configuration, pyverless support
  3 different types of parameters, `region`, `stage` and `region & stage`
- **Type-Hinting** - with `pyverless` you will get an out-of-the-box solution to understand what kind of attributes are
  supported in `serverless` in one place.

### Usage:

by default the `pyls MODULE` command will generate a `serverless.yml` file in the current directory.

*running*: `pyls main:sls && sls print --region us-east-1 --stage dev`

for example will generate `serverless.yml` file and print the serverless output when `region` is `us-east-1` and `stage`
is `dev`

### Contributing:

We love our contributors! Please read our Contributing Document to learn how you can start working on the Framework
yourself.