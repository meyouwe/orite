import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="orite",
    version="0.0.16",
    author="Maarten Idema",
    author_email="maarten@mountdeluxe.com",
    description="orite - an opinionated Python rsync wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meyouwe/orite",
    # packages=setuptools.find_packages(),
    packages=['orite'],
    include_package_data=True,
    entry_points = {
        'console_scripts': ['orite=orite.command_line:main'],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet"
    ),
)

# Build with
# $ python3 setup.py sdist bdist_wheel
# Upload to the Pypi with twine
# $ twine upload dist/*