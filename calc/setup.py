import os
from setuptools import setup, find_packages

def read(fname):
    """Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="nuros-calculator",
    version="1.0.0",
    author="AnmiTaliDev",
    author_email="anmitali@anmitali.kz",
    description="NurOS Calculator with Delta Design Concept Night theme",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    license="GPL-3.0",
    keywords="calculator, pyqt6, nuros, deltadesign, dde",
    url="https://github.com/nuros-linux/ddeapps",
    
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    package_data={
        "calculator": [
            "resources/icons/*.png",
            "resources/icons/*.svg",
            "resources/*.desktop",
        ],
    },
    
    data_files=[
        ('share/applications', ['src/calculator/resources/nuros-calculator.desktop']),
        ('share/icons/hicolor/symbolic/apps', 
         ['/usr/share/icons/Adwaita/symbolic/apps/org.gnome.Calculator-symbolic.svg']),
        ('share/doc/nuros-calculator', ['README.md', 'LICENSE']),
    ],
    
    python_requires='>=3.8',
    install_requires=[
        'PyQt6>=6.4.0',
        'requests>=2.31.0',
    ],
    
    entry_points={
        'console_scripts': [
            'nuros-calculator=calculator.main:main',
        ],
        'gui_scripts': [
            'nuros-calculator-gui=calculator.main:main',
        ],
    },
    
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    
    zip_safe=False,
    platforms=['Linux'],
)