from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="braidgenerator",
    version="1.0.0",
    description="Braid Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Algebra8/Knots",
    author="Braid Generator Team",
    author_email="mmnasrollahi@ucdavis.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pandas"],
    extras_require={
        'tests': ['unittest'],
    },
)
