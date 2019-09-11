import setuptools

setuptools.setup(
    name="awswizard",
    version='0.0.2',
    author="aws wizard",
    author_email="st.kurilin@gmail.com",
    description="Amazon made simple.",
    long_description="aws-wizard.com",
    long_description_content_type="text/markdown",
    url="https://aws-wizard.com",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
