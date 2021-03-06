#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = [
    'Click>=6.0',
    'joblib>=0.13.2',
    'numpy',
    'pandas',
    'requests',
    'scikit-learn',
    'sklearn',
    'pathlib',
]

setup_requirements = [ ]

test_requirements = [
    'pytest',
]

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
