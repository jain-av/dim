from setuptools import setup

setup(
    name="dim-bind-file-agent",
    version="0.1",
    packages=['dim_bind_file_agent'],  # add this line
    py_modules=['dim_bind_file_agent'], # and remove this line
    install_requires=["dimclient==0.2", "argparse"],
    entry_points={
        'console_scripts': [
            'dim-bind-file-agent = dim_bind_file_agent:main',
        ],
    },
)
