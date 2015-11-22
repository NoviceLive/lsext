"""
Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>
"""


from setuptools import setup


setup(
    name='lsext',
    version='0.1.0',
    packages=['lsext'],
    entry_points={
        'console_scripts' : ['lsext=lsext.start:main']
    },

    author='Gu Zhengxiong',
    author_email='rectigu@gmail.com',
    description='File Extension Distribution Analysis',
    keywords='List Extensions, Traverse Directories',
    license='GPL',
    url='https://github.com/NoviceLive/lsext',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
