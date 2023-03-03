#!/usr/bin/env -S docker image build -t iacopilot . -f

FROM        python:3

WORKDIR     /app

ENTRYPOINT  ["iacopilot"]

RUN         pip install \
              internetarchive \
              llama-index \
              openai \
              pydantic \
              requests \
              rich

COPY        . ./
RUN         python3 setup.py install
