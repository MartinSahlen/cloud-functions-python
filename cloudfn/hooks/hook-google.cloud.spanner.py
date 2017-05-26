from PyInstaller.utils.hooks import copy_metadata

datas = copy_metadata('google-cloud-spanner')
datas += copy_metadata('google-cloud-core')
