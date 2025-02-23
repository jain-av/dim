from setuptools import setup

setup(
    name='dim-cas',
    packages=['cas'],
    data_files=[
        ('share/dim-cas', ['cas.wsgi', 'cas/config.py.example'])
    ],
    version='2.0',  # Assuming a fixed version for migration
    install_requires=[
        'xmltodict',
        'flask',
        'requests'
    ],
)
