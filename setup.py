
import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='flasky-settings',
    version='0.0.1.5',
    url='https://github.com/LordBex/flasky-settings',
    license='',
    author='lordbex',
    author_email='lordibex@protonmail.com',
    description='Flask extension that includes a Settings-Manager in your project',
    long_description=read('README.rst'),
    packages=['flasky_settings', 'flasky_settings.settings', 'flasky_settings.elements', 'flasky_settings.forms'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=2.2.2'
    ],
    classifiers=[
        'Environment :: Web Environment', 'Intended Audience :: Developers',
        'Operating System :: OS Independent', 'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ])