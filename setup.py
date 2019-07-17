#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = [
    'Click>=6.0',
    'certifi==2019.6.16',
    'chardet==3.0.4',
    'idna==2.8',
    'joblib==0.13.2',
    'numpy==1.16.4',
    'pandas==0.24.2',
    'python-dateutil==2.8.0',
    'pytz==2019.1',
    'requests==2.22.0',
    'responses==0.10.6',
    'scikit-learn==0.21.2',
    'scipy==1.3.0',
    'six==1.12.0',
    'sklearn==0.0',
    'urllib3==1.25.3',
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Tom Hudson",
    author_email='tom@vectorspace.co',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Score and label proposals .",
    entry_points={

    },
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='nesta_score_label',
    name='nesta_score_label',
    packages=find_packages(include=['nesta_score_label']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/audreyr/nesta_score_label',
    version='0.1.0',
    zip_safe=False,
)
