#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for Batı Karadeniz Orman İzleme Sistemi
Kurulum: python setup.py install
Geliştirme: pip install -e .
"""

from setuptools import setup, find_packages
import os

# README dosyasını oku
def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, encoding='utf-8') as f:
            return f.read()
    return ''

# Bağımlılıklar
INSTALL_REQUIRES = [
    'numpy>=1.21.0',
    'pandas>=1.3.0',
    'scipy>=1.7.0',
    'matplotlib>=3.4.0',
    'plotly>=5.0.0',
    'seaborn>=0.11.0',
]

# Opsiyonel bağımlılıklar
EXTRAS_REQUIRE = {
    'gee': ['earthengine-api>=0.1.300', 'geemap>=0.15.0'],
    'gis': ['rasterio>=1.2.0', 'geopandas>=0.9.0', 'shapely>=1.7.0'],
    'jupyter': ['jupyter>=1.0.0', 'jupyterlab>=3.0.0', 'notebook>=6.4.0'],
    'dev': ['pytest>=6.2.0', 'black>=21.7b0', 'pylint>=2.10.0'],
    'full': [
        'earthengine-api>=0.1.300',
        'geemap>=0.15.0',
        'rasterio>=1.2.0',
        'geopandas>=0.9.0',
        'shapely>=1.7.0',
        'jupyter>=1.0.0',
        'jupyterlab>=3.0.0',
    ]
}

setup(
    name='bati-karadeniz-orman-izleme',
    version='1.0.0',
    description='Batı Karadeniz Bölgesi Orman Değişim Analizi ve Afet Yönetimi',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    
    author='Ernozkn',
    author_email='ernozkn@gmail.com',
    url='https://github.com/Ernozkn/Bati-Karadeniz-Orman-Izleme',
    
    license='MIT',
    
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    
    keywords='gis remote-sensing sentinel earth-engine forest management',
    
    project_urls={
        'Bug Reports': 'https://github.com/Ernozkn/Bati-Karadeniz-Orman-Izleme/issues',
        'Source': 'https://github.com/Ernozkn/Bati-Karadeniz-Orman-Izleme',
        'Documentation': 'https://github.com/Ernozkn/Bati-Karadeniz-Orman-Izleme/wiki',
    },
)
