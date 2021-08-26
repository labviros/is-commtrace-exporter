from setuptools import setup, find_packages

setup(
    name='is_commtrace_exporter',
    version='0.0.1',
    description='',
    url='http://github.com/wagnercotta/is-commtrace-exporter',
    author='wagner',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': ['is-commtrace-exporter=is_commtrace_exporter.service:main',],
    },
    zip_safe=False,
    install_requires=[
       'opencensus-ext-zipkin==0.2.1',
    ],
)

