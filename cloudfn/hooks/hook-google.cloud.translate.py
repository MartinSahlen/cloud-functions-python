from PyInstaller.utils.hooks import copy_metadata

datas = copy_metadata('google-cloud-translate')
datas += copy_metadata('google-cloud-core')
datas += copy_metadata('google-api-core')
