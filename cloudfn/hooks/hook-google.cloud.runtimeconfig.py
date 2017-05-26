from PyInstaller.utils.hooks import copy_metadata

datas = copy_metadata('google-cloud-runtimeconfig')
datas += copy_metadata('google-cloud-core')
