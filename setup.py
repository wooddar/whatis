from setuptools import setup, find_packages
from whatis import __version__

# Get requirements for dependencies
requirements = open("requirements.txt").read().split("\n")

setup(
    name="whatis-bot",
    version=__version__,
    packages=find_packages(),
    url="https://github.com/wooddar/whatis",
    license="mit",
    author="Hugo Darwood",
    scripts=["scripts/whatis-serve"],
    author_email="hugodarwood@gmail.com",
    description="A Slack app to explore, create and curate your workspace's business terminology",
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
