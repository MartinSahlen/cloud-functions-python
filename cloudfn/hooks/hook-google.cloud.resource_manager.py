from PyInstaller.utils.hooks import copy_metadata

datas = copy_metadata('google-cloud-resource-manager')
datas += copy_metadata('google-cloud-core')
