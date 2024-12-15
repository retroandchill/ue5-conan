from setuptools import setup, find_packages

setup(
    name='ue5-conan',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/retroandchill/ue5-conan',
    author='Retro & Chill',
    description='UE5 Conan helper library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'conan>=2.10.1',
        'pydantic>=2.10.3',
        'pystache >= 0.6.6'
    ],
    include_package_data=True,
    package_data={
        'ue5_conan': ['**/*.mustache']
    }
)