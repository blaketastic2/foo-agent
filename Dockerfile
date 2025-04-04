ARG PYTHON_VERSION=3.11

FROM python:$PYTHON_VERSION-slim-bookworm AS agent-slim

ARG FLYTEKIT_VERSION=1.14.0b6
RUN if [ -z "$FLYTEKIT_VERSION" ]; then echo "FLYTEKIT_VERSION is not set"; exit 1; fi

LABEL org.opencontainers.image.authors="Flyte Team <users@flyte.org>"
LABEL org.opencontainers.image.source=https://github.com/flyteorg/flytekit

RUN apt-get update && apt-get install build-essential -y

RUN pip install --upgrade uv
RUN pip install prometheus-client grpcio-health-checking==1.67.1
RUN pip install --no-cache-dir -U flytekit==${FLYTEKIT_VERSION} \
  && apt-get clean autoclean \
  && apt-get autoremove --yes \
  && rm -rf /var/lib/{apt,dpkg,cache,log}/ \
  && :

FROM agent-slim AS agent-all
ARG FLYTEKIT_VERSION

COPY requirements.txt requirements.txt
RUN python -m uv pip install -r requirements.txt
COPY dist/*.whl /tmp/
RUN ls -al /tmp/
RUN python -m uv pip install --no-cache-dir --no-index /tmp/*.whl

ENV FLYTE_SDK_LOGGING_LEVEL=10

CMD ["pyflyte", "serve", "agent", "--port", "8000"]