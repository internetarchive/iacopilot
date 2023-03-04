import setuptools

from iacopilot import __NAME, __VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=__NAME.lower(),
    version=__VERSION,
    author="Sawood Alam",
    author_email="sawood@archive.org",
    description="Summarize and ask questions about items in the Internet Archive",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/internetarchive/iacopilot",
    packages=setuptools.find_packages(),
    provides=[
        "iacopilot"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Archiving",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search"
    ],
    python_requires='>=3.6',
    install_requires=[
        "internetarchive",
        "llama-index",
        "openai",
        "pydantic",
        "requests",
        "rich"
    ],
    zip_safe=True,
    entry_points={
        "console_scripts": [
            "iacopilot = iacopilot.__main__:main"
        ]
    }
)
