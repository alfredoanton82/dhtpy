import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dhtpy",
    version="0.0.1",
    author="A. M. Anton",
    author_email="",
    description="DHT sensor library in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alfredoanton82/dhtpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
