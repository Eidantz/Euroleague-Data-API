from setuptools import setup, find_packages

setup(
    name="Euroleague-Data-API", 
    version="0.1.0", 
    description="A GraphQL API client for the Euroleague statistics and game data",
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",
    author="Eidan Tzdaka",
    author_email="eidantz@gmail.com",
    url="https://github.com/Eidantz/Euroleague-Data-API",
    packages=find_packages(),
    install_requires=[
        "strawberry-graphql",
        "requests",
        "uvicorn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11', 
)
