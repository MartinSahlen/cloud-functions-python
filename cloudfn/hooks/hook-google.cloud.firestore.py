from PyInstaller.utils.hooks import copy_metadata

datas = copy_metadata('google-cloud-firestore')
datas += copy_metadata('google-cloud-core')
datas += copy_metadata('google-api-core')
