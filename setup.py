from setuptools import setup

setup(
    name="Lipid Wizard",
    version="1.0",
    author="Raobo Xu & Huan Liu",
    description="",
    packages=["lipidTask"],
    install_requires=[
        "PySide6",
        "openpyxl",
        "numpy",
        "matplotlib",
        "requests",
        "brain-isotopic-distribution",
        "scipy",
    ],
    entry_points={
        "console_scripts": [
            "my_script = lipidTask.gui:main",
        ],
    },
)