import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="monteprediction",
    version="0.0.3",
    description="A Weekly Monte Carlo Game",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/microprediction/monteprediction",
    author="microprediction",
    author_email="peter.cotton@microprediction.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["monteprediction"],
    test_suite='pytest',
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=['numpy','pandas','yfinance'],
    entry_points={
        "console_scripts": [
            "monteprediction=monteprediction.__main__:main",
        ]
    },
)