from setuptools import setup, find_packages

setup(
    name = 'pyvcs',
    version = '0.1',
    packages = find_packages('pyvcs'),
    package_dir = {'': 'pyvcs'},
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Version Control'
    ],
)
