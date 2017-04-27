docker run --rm -ti -v $(pwd):/app lol /bin/sh -c 'cd app && pyinstaller test.py -y -n func' && \
gcloud beta functions deploy hello --trigger-http --entry-point serve --stage-bucket cloudfuncbucket --memory 2048MB
