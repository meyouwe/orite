import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="orite",
    version="0.0.3",
    author="Maarten Idema",
    author_email="maarten@mountdeluxe.com",
    description="orite.py – is an opinionated Python rsync wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meyouwe/orite",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)