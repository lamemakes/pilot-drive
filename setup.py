from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pilot-drive",
    version="0.10.1",
    author="Wesley Appler",
    author_email="wes@lamemakes.com",
    description="PILOT Drive is a modular vehicle head unit built in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lamemakes/pilot-drive",
    project_urls={
        "Bug Tracker": "https://github.com/lamemakes/pilot-drive/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Unix",
    ],
    install_requires=["flask", "obd"],
    packages=["pilot_drive", "pilot_drive.utils"],
    include_package_data=True,
    package_data={"pilot_drive": ["pilot_drive/web/*", "tests/*"]},
    entry_points={'console_scripts' : ["pilot-drive=pilot_drive.main:main"]},
    python_requires=">=3.6",
)
