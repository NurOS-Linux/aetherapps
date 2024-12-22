"""
NurOS Media Player - Setup
~~~~~~~~~~~~~~~~~~~~~
DeltaDesign Concept Night Setup Script

Created: 2024-12-22 11:07:37 UTC 
Author: AnmiTaliDev
License: GPL 3
"""

from setuptools import setup, find_packages

setup(
    name="nuros-mediaplayer",
    version="1.0.0",
    author="AnmiTaliDev",
    description="DeltaDesign Concept Night Media Player",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.5.0",
        "PyQt6-Qt6>=6.5.0",
        "PyQt6-sip>=13.5.0",
        "mutagen>=1.46.0",
        "numpy>=1.24.0",
        "sounddevice>=0.4.6"
    ],
    entry_points={
        "console_scripts": [
            "nuros-mediaplayer=mediaplayer.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "mediaplayer": ["assets/*"],
    },
)