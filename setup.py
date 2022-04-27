import subprocess

from setuptools import setup
from setuptools import find_packages


with open("Readme.md", "r") as f:
    long_description = f.read()


setup(
    name='sevak',
    version='v0.0.1',
    description="Your Raspi's sevak, can streams video from a raspi.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/jalotra/sevak',
    author='jalotra',
    keywords=['wheels'],
    package_dir = {"" : "sevak"},
    packages=find_packages(where = "sevak", exclude=['tests']),
    install_requires=[
        'logzero',
        'paho-mqtt', 
        'opencv-python'
    ],
    python_requires='>=3',  

    entry_points={
        'console_scripts': [
            'bn_camera=sevak.service.camera_service.camera_service:main'
        ]
    },

    test_suite='tests'
)
