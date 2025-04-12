from setuptools import setup

from benchmark import __VERSION__

setup(
    name='benchmark',
    version=__VERSION__,
    url='https://github.com/JeffSpies/benchmark',
    license='LICENSE.txt',
    author='Jeffrey R. Spies',
    author_email='code@jeffspies.com',
    description='Python benchmarker / benchmarking framework',
    long_description=open('README.txt').read(),
    packages=['benchmark'],
    install_requires=[],
    tests_require = ['tox', 'pytest', 'six>=1.8'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Benchmark",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ]
)
