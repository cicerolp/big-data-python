from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='dextra-big-data-python',
    version='1.0.0',
    author='Cícero Augusto de Lara Pahins',
    author_email='cicerolp@gmail.com',
    description='Application to Resolve Dextra\'s Programming Challange.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.7'
)
