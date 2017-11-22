#!/bin/bash
py-cloud-fn $FUNC_NAME http --python_version ${PYTHON_VERSION:-2.7} -p -f function.py && \
cd cloudfn/target && gcloud beta functions deploy $FUNC_NAME \
--trigger-topic $TRIGGER_TOPIC --stage-bucket $STAGE_BUCKET --memory 2048MB && cd ../..
