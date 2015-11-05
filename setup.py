import os
import iglobal
from setuptools import setup, find_packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


setup(
    name='python-iglobal',
    version=iglobal.__version__,
    author='Ridley Larsen',
    author_email='ridley@iglobalstores.com',
    keywords='iglobal api',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    url='https://github.com/iGlobal/python-iglobal',
    description=' '.join(__import__('iglobal').__doc__.splitlines()).strip(),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    long_description=read_file('README.md'),
    test_suite="runtests.runtests",
    zip_safe=False,
    install_requires=['requests', 'six']
)
