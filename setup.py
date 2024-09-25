from setuptools import setup, find_packages

setup(
    name="recruit_repo",
    version="0.1.0",
    packages=find_packages(include=['agent', 'api', 'config', 'graphs', 'processing']),
    install_requires=[
        # Add dependencies in future
    ],
)