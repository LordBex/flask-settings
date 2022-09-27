
import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='flask-settings',
    version='0.0.1',
    url='https://github.com/LordBex/flask-settings',
    license='',
    author='lordbex',
    author_email='lordibex@protonmail.com',
    description='Flask extension that includes a Settings-Manager in your project',
    long_description=read('README.md'),
    packages=['flask_settings', 'flask_settings.settings'],
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