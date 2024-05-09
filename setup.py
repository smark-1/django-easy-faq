import os

from setuptools import setup
from os import path

install_requires = [
    "Django>=3.2",
]

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
        name="django-easy-faq",
        version=os.environ.get("RELEASE_VERSION", '0.0.1'),
        description="A Django app to add great FAQ functionality to website",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/smark-1/django-easy-faq/",
        download_url="https://pypi.python.org/pypi/django-easy-faq",
        license="MIT",
        packages=["faq"],
        install_requires=install_requires,
        include_package_data=True,
        python_requires=">=3.9",
        keywords=[
            "django",
            "faq",
        ],
        classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Framework :: Django",
        ],
)