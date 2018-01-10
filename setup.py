"""
"""
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='PyNagCore',
    version='0.1.5',
    description='An python module for basic nagios core command handling',
    author='noelmcloughlin',
    author_email='noel.mcloughlin@gmail.com',
    license='Apache 2.0',
    long_description=open('README.md').read(),
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='Nagios Core',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    # To distribute just a my_module.py, uncomment #py_modules=["my_module"],

    install_requires=required,
    setup_requires=[]
)
