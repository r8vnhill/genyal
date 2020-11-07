import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="genyal",  # Replace with your own username
    version="0.1.11.1",
    author="Ignacio Slater Muñoz",
    author_email="islaterm@gmail.com",
    description="A framework for genetic algorithms in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/islaterm/genyal",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: Creative Commons Attribution 4.0 International License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
