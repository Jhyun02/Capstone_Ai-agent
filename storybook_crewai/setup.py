from setuptools import setup, find_packages

setup(
    name="storybook_crewai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "moviepy",
        "crewai",
        "crewai-tools",
        "python-dotenv",
    ],
) 