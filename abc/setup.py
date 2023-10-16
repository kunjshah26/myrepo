import setuptools

setuptools.setup(
    name="unilever_map_lib",
    version="0.0.1",
    author="Kunj Shah",
    author_email="Kunj.Shah@unilever.com",
    description="POC",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
    'pyspark',
    'spark'
]
)
