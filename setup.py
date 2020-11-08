#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

setuptools.setup(
    name='photoprism_face_recognition',
    packages=['my_project'],
    install_requires=install_requires
)
