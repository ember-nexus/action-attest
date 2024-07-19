FROM python:3.12-alpine3.20 as base

FROM base as development

RUN apk add bash curl wget jq
WORKDIR /app

FROM base as production-build

WORKDIR /app
COPY src src
COPY pyproject.toml pyproject.toml
RUN pip install .

FROM scratch as production

COPY --from=production-build / /
WORKDIR /app
ENTRYPOINT ["python", "-m", "src"]
