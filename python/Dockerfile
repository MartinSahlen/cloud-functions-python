FROM ubuntu
# Update
RUN apt-get update
RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN apt-get install -y curl
RUN curl https://sdk.cloud.google.com | bash
RUN ~/google-cloud-sdk/bin/gcloud -q components install alpha
RUN ~/google-cloud-sdk/bin/gcloud -q components install beta
RUN ~/google-cloud-sdk/bin/gcloud -q components install kubectl

# Install app dependencies
RUN pip install --upgrade pip
RUN pip install virtualenv
