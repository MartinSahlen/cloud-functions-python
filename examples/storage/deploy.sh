#!/bin/bash
py-cloud-fn $FUNC_NAME bucket -p --python_version ${PYTHON_VERSION:-2.7} -f function.py && \
cd cloudfn/target && gcloud beta functions deploy $FUNC_NAME \
--trigger-bucket $TRIGGER_BUCKET --stage-bucket $STAGE_BUCKET --memory 2048MB && cd ../..
