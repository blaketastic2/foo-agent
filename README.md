# Foo Agent

This is a sample agent designed to demonstrate returning complex data as output from an agent.

# Local Dev

create the venv:

```bash
uv venv
source .venv/bin/activate
```

install/update deps:

```bash
uv pip compile requirements.in -o requirements.txt
uv pip install -r requirements.txt
```

ensure the Flyte Sandbox is running w/

```bash
flytectl demo start
```

build project and docker image, then push:

```bash
uv build
docker buildx build --platform linux/amd64 \
  -t localhost:30000/flyteagent:local \
  --build-arg PYTHON_VERSION=3.11 \
  --build-arg FLYTEKIT_VERSION=1.15.1 \
  -f Dockerfile . --load
  
docker push localhost:30000/flyteagent:local
```

update deployment, point to local image:

```bash
k set image deployment/flyteagent flyteagent=localhost:30000/flyteagent:local
k patch deployment flyteagent -p '{"spec": {"template": {"spec": {"containers": [{"name": "flyteagent", "imagePullPolicy": "Always"}]}}}}'
```

restart deployment:

```bash
k rollout restart deployment flyteagent
```

run example:

```bash
pyflyte run --remote --copy all -p flytesnacks -d development src/foo.py foo_wf
```