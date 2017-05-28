py-cloud-fn $FUNC_NAME http -p -f flask.py && \
cd cloudfn/target && gcloud beta functions deploy $FUNC_NAME \
--trigger-http --stage-bucket $STAGE_BUCKET --memory 2048MB && cd ../..
