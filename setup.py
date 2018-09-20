from setuptools import setup, find_packages
import re


def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)


setup(
    name="gwe",
    version=get_property("__version__", "gwe"),
    description="Grid World Engine package",
    author="liyue",
    url="https://github.com/liyue6174/GridWorldEngine.git",
    packages=find_packages(),
    package_data={"gwe": ["font/*.*"]},
    install_requires=[
        "pygame==1.9.4",
        "numpy==1.15.1",
        "scipy==1.1.0"
    ]
)
