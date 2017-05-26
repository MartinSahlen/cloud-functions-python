rm -rf build
rm -rf dist
rm -rf pycloudfn.egg-info
python setup.py sdist bdist_wheel
twine upload dist/*
