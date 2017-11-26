FROM ubuntu:17.10

# Update
RUN \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive \
    apt-get install -y \
      python2.7 \
      python-pip \
  && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Install app dependencies
RUN pip install pip==9.0.1
RUN pip install virtualenv==15.1.0
