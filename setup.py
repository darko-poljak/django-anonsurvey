import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-anonsurvey',
    version='0.2.1',
    packages=['anonsurvey'],
    include_package_data=True,
    license='GPLv3',
    description='A Django app to create Web-based anonymous surveys',
    long_description=README,
    install_requires=["django-tinymce", "Django-tinymce-filebrowser"],
    url='https://github.com/darko-poljak/django-anonsurvey',
    author='Darko Poljak',
    author_email='darko.poljak@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
