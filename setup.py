from pkg_resources import parse_requirements
from setuptools import setup

NAME = 'plex-anime-replacer'
VERSION = '0.5.2'
DESCRIPTION = 'Replacer for names and locations of anime files downloaded from ru-fandub trackers'
MODULES = ['replacer', 'replacer.filesystem', 'replacer.settings']


def load_requirements(filename: str) -> list:
    with open(filename, 'r', encoding="utf-8") as file:
        return [f"""{req.name}{f"[{','.join(req.extras)}]" if req.extras else ''}{req.specifier}"""
                for req in parse_requirements(file.read())]


setup(
    name=NAME,
    version=VERSION,
    packages=MODULES,
    url='https://git.fkinuo.ru/plex-anime-replacer',
    license='MIT',
    author='Firin Kinuo',
    author_email='deals@fkinuo.ru',
    description=DESCRIPTION,
    install_requires=load_requirements('requirements.txt'),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'anime-replacer = replacer.__main__',
        ]
    },
)
