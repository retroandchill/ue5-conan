from setuptools import setup

setup(
    name='ue5-conan',
    version='0.1.0',
    packages=['ue5_conan'],
    url='https://github.com/retroandchill/ue5-conan',
    author='Retro & Chill',
    description='UE5 Conan helper library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'conan>=2.9.2'
    ],
)