from distutils.core import setup

setup(
    name='GA_lite',
    version='0.1.0',
    author='Val Lyashov',
    author_email='val@plstr.com',
    packages=['ga_lite', 'ga_lite.test'],
    url='http://pypi.python.org/pypi/ga_lite/',
    license='LICENSE.txt',
    description='A lite Google Analytics Data Export API library.',
    long_description=open('README.txt').read(),
    install_requires=[
        'requests >= 0.11.0',
        'pysqlite >= 2.0.0'
    ],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ),
)