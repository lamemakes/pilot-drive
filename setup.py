import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pilot-auto-lamemakes",
    version="0.1.0",
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
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)