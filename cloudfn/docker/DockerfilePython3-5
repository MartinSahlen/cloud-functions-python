FROM ubuntu:16.04

# Update
RUN \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive \
    apt-get install -y \
      python3.5 \
      python3-pip \
  && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Install app dependencies
RUN python3.5 -m pip install pip==9.0.1
RUN python3.5 -m pip install virtualenv==15.1.0
