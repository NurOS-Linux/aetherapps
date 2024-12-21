import os
import sys
from setuptools import setup, find_packages
from datetime import datetime

# Project metadata
VERSION = '1.0.0'
BUILD_DATE = "2024-12-21"
AUTHOR = "AnmiTaliDev"
EMAIL = "anmitali@anmitali.kz"
REPO_URL = "https://github.com/nuros-linux/ddeapps"

def read(fname):
    """Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# Core dependencies
REQUIRED_PACKAGES = [
    'PyQt6>=6.4.0',
    'requests>=2.31.0',
]

# Development dependencies
DEVELOPMENT_PACKAGES = [
    'pytest>=7.4.0',
    'black>=23.0.0',
    'pylint>=2.17.0',
    'pyinstaller>=6.0.0',
]

setup(
    # Basic package information
    name="nuros-calculator",
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description="NurOS Calculator with Delta Design Concept Night theme",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    license="GPL-3.0",
    keywords="calculator, pyqt6, nuros, deltadesign, dde",
    url=REPO_URL,
    
    # Package discovery
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    # Package data and resources
    package_data={
        "calculator": [
            "resources/icons/*.png",
            "resources/icons/*.svg",
            "resources/*.desktop",
        ],
    },
    
    # System files installation
    data_files=[
        ('share/applications', ['src/resources/nuros-calculator.desktop']),
        # Using GNOME Calculator icon from Adwaita
        ('share/icons/hicolor/symbolic/apps', 
         ['/usr/share/icons/Adwaita/symbolic/apps/org.gnome.Calculator-symbolic.svg']),
        ('share/doc/nuros-calculator', ['README.md', 'LICENSE']),
    ],
    
    # Dependencies
    install_requires=REQUIRED_PACKAGES,
    extras_require={
        'dev': DEVELOPMENT_PACKAGES,
    },
    
    # Entry points
    entry_points={
        'console_scripts': [
            'nuros-calculator=calculator.main:main',
        ],
        'gui_scripts': [
            'nuros-calculator-gui=calculator.main:main',
        ],
    },
    
    # Package metadata
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: POSIX :: Linux',
        'Environment :: X11 Applications :: Qt',
        'Natural Language :: English',
    ],
    
    python_requires='>=3.8',
    
    project_urls={
        'Bug Reports': f'{REPO_URL}/issues',
        'Source': REPO_URL,
        'Documentation': f'{REPO_URL}/wiki',
    },
    
    include_package_data=True,
    
    # Build options
    options={
        'build_exe': {
            'includes': ['PyQt6'],
            'include_files': [
                ('src/resources', 'resources'),
            ],
            'build_exe': 'build/calculator',
        },
    },
    
    zip_safe=False,
    platforms=['Linux'],
    
    # Build information
    build_info={
        'build_date': BUILD_DATE,
        'builder': AUTHOR,
    },
)