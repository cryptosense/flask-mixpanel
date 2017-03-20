from setuptools import find_packages, setup

version = '0.1.0'

setup(
    name='flask-mixpanel',
    packages=find_packages(exclude=('tests', 'docs')),
    version=version,
    description='Wrappers for using Mixpanel in Flask',
    long_description=open('README.rst', 'r').read(),
    author='Bertrand Bonnefoy-Claudet',
    author_email='bertrand@cryptosense.com',
    url='https://github.com/cryptosense/flask-mixpanel',
    download_url='https://github.com/cryptosense/flask-mixpanel/tarball/v{}'.format(version),
    keywords=['web', 'server', 'analytics'],
    license='BSD',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    install_requires=[
        'Flask',
        'mixpanel',
        'mixpanel-py-async',
    ],
)
