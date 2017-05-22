FROM ubuntu
# Update
RUN apt-get update
RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN apt-get install -y curl

# Install app dependencies
RUN pip install --upgrade pip
RUN pip install virtualenv
