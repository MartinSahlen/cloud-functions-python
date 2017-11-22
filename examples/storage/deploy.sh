py-cloud-fn $FUNC_NAME bucket -p -f function.py && \
cd cloudfn/target && gcloud beta functions deploy $FUNC_NAME \
--trigger-bucket $TRIGGER_BUCKET --stage-bucket $STAGE_BUCKET --memory 2048MB && cd ../..
