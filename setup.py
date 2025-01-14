from setuptools import find_packages, setup

setup(
    name="apparun",
    version="0.3.0",
    author="Maxime Peralta",
    author_email="maxime.peralta@cea.fr",
    description="Appa Run is a package to execute impact models produced by Appa Build",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "apparun=app.cli.main:cli_app",
        ],
    },
)
