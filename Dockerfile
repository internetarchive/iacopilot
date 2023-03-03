#!/usr/bin/env -S docker image build -t iacopilot . -f

FROM        python:3

WORKDIR     /app

ENTRYPOINT  ["./main.py"]

RUN         pip install \
              internetarchive \
              llama-index \
              openai \
              pydantic \
              rich

COPY        . ./
