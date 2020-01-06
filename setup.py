# vim:fileencoding=utf-8:noet

import io
from os import path

from setuptools import setup

version = "0.1"

this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="powerline-timewarrior",
    description="Powerline segments for showing information from the Timewarrior time tracker",
    version=version,
    keywords="powerline timewarrior prompt",
    license="MIT",
    author="Guillerme Duvillié",
    author_email="guillerme@duvillie.eu",
    url="https://github.com/MFreeze/powerline-timewarrior",
    download_url="https://github.com/MFreeze/powerline-timewarrior/tarball/{version}".format(version=version),
    packages=["powerline-timewarrior"],
    install_requires=["powerline-status"],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Terminals",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
