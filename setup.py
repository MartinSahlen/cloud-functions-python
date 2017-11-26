from setuptools import setup

setup(
    name='pycloudfn',
    version='0.1.207',
    description='GCP Cloud functions in python',
    url='https://github.com/MartinSahlen/cloud-functions-python',
    author='Martin Sahlen',
    author_email='martin8900@gmail.com',
    license='MIT',
    entry_points={
        'console_scripts': ['py-cloud-fn=cloudfn.cli:main'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=[
        'pyinstaller==3.2.1',
        'python-dateutil==2.6.0',
        'werkzeug==0.12',
        'django==1.11.1',
        'six==1.10.0',
        'Jinja2==2.9.6',
        'pyspin==1.1.1',
        'google-auth==1.0.1',
    ],
    include_package_data=True,
    packages=['cloudfn'],
    zip_safe=False
)
