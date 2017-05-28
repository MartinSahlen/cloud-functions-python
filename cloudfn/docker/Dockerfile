FROM ubuntu
# Update
RUN apt-get update
RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN apt-get install -y curl

# Install app dependencies
RUN pip install pip==9.0.1
RUN pip install virtualenv==15.1.0
RUN pip install pyinstaller==3.2.1
