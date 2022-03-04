import os

from setuptools import find_packages, setup

cwd = os.path.dirname(os.path.realpath(__file__))
file = os.path.join(cwd, 'requirements.txt')
with open(file) as f:
    dependencies = list(map(lambda x: x.replace("\n", " "), f.readlines()))

setup(
    name='hand-crafted-models',
    version='1.0',
    description='Hand-crafted discriminative linear predictive models',
    author='Samuel Luo',
    author_email='viridis959@gmail.com',
    url='https://github.com/viridis959',
    install_requires=dependencies,
    packages=find_packages(),
)
