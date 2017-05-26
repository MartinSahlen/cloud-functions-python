from PyInstaller.utils.hooks import copy_metadata

datas = copy_metadata('google-cloud-error-reporting')
datas += copy_metadata('google-cloud-core')
