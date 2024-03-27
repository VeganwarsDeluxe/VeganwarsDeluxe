from setuptools import setup, find_packages
from VegansDeluxe import core

setup(
    name='VegansDeluxe',
    version=core.__version__,
    author='vezono',
    author_email='vezono@gts.org.ua',
    url='https://onedev.gts.org.ua/vezono/vegans-deluxe',
    packages=find_packages(include="VegansDeluxe"),
    package_data={'': ['localizations']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12'
)
