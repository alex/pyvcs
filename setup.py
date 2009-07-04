from setuptools import setup, find_packages

setup(
    name = 'pyvcs',
    version = '0.1',
    description = "A lightweight abstraction layer over multiple VCSs.",
    url = 'http://github.com/alex/pyvcs/',
    packages = find_packages('pyvcs'),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Version Control'
    ],
)
