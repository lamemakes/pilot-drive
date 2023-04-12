from setuptools import setup, find_packages
from pilot_drive import __version__ as pilot_version

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pilot-drive",
    version=pilot_version,
    author="lamemakes",
    author_email="wes@lamemakes.com",
    description="PILOT Drive is a modular vehicle head unit built in Python",
    license="GNU GPL v3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lamemakes/pilot-drive",
    project_urls={
        "Documentation": "https://pilot-drive.readthedocs.org",
        "Bug Tracker": "https://github.com/lamemakes/pilot-drive/issues",
    },
    install_requires=["websockets", "obd", "requests", "dbus-python==1.2.16", "PyGObject"],
    entry_points={"console_scripts": ["pilot-drive = pilot_drive.__main__:run"]},
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    python_requires=">=3.9",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3.11"
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
)
