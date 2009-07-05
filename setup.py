from setuptools import setup, find_packages

setup(
    name = 'pyvcs',
    version = '0.1',
    author = 'Alex Gaynor, Justin Lilly',
    author_email = 'alex.gaynor@gmail.com',
    description = "A lightweight abstraction layer over multiple VCSs.",
    url = 'http://github.com/alex/pyvcs/',
    packages = find_packages(),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Version Control'
    ],
)
