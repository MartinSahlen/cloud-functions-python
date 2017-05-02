# WIP

Getting python running in cloud functions

## Concept
- Use learnings from https://github.com/MartinSahlen/go-cloud-fn/
- Use https://github.com/pyinstaller/pyinstaller to bundle python package for fast execution
- Use docker/ubuntu + virtualenv + requirements.txt to install and bundle dependencies. Need to build in docker because pyinstaller is platform-dependent, and cloud functions is executed in a linux/ubuntu environment.
