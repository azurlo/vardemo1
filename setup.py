import setuptools


setuptools.setup(
    name='vardemo1',
    version='0.0.1',
    description='Monte-Carlo simulation for stock prices behaviour based on data from www.quandl.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    packages=[
        'vardemo1',
    ],
    install_requires=[
        'matplotlib',
        'numpy',
        'quandl',
    ],
    entry_points={
        'console_scripts': [
            'randomwalk=vardemo1.randomwalk:main',
        ],
    },
)
