from setuptools import setup, find_packages

setup(
    name='django-template-email',
    version='0.1',
    author='Ben Davis',
    author_email='code@bendavismedia',
    url='http://github.com/bendavis78/django-template-email',
    description=('A useful tool for building email messages using django '
                 'templates'),
    keywords='savid',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(),
    include_package_data=True
)
