from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pilot-drive",
    version="0.10.0",
    author="Wesley Appler",
    author_email="wes@lamemakes.com",
    description="PILOT Auto is a modular vehicle head unit built in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lamemakes/pilot-auto",
    project_urls={
        "Bug Tracker": "https://github.com/lamemakes/pilot-auto/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Unix",
    ],
    install_requires=["flask", "obd"],
    package_data={"pilot-drive": ["src/web/*", "tests/*"]},
    packages=find_packages(include=["src", "src.*"]),
    #entry_points={'console_scripts' : ["pilot-drive=pilot-drive.main:main"]},
    python_requires=">=3.6",
)
