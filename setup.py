from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name="visvmtagger",
    version="1.0a0",
    description="SVM based Vietnamese tokenize and part-of-speech tagger",
    long_description="",
    author="Kanji Takahashi",
    license="MIT",
    url="https://github.com/kanjirz50/viet-morphological-analysis-svm/",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=["scikit-learn>=0.19", "logzero>=1.5", "pytest", "numpy", "scipy"],
    dependency_links=[],
    python_requires='~=3.6',
    include_package_data=True,
 )
