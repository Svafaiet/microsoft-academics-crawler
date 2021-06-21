import setuptools

setuptools.setup(
    name="microsoftaca",
    version="0.4.0",
    author="Soroush Vafaie Tabar",
    author_email="svafaiet @gmail.com",
    description="CLI microsoft academia recommender",
    packages=setuptools.find_packages(exclude=("tests.*",)),
    install_requires=[
        "Twisted==19.10.0",
        "Scrapy==1.8.0",
        "scrapy-splash==0.7.2",
        "fake-useragent==0.1.11",
        "numpy==1.19.2",
        "typer>=0.3, <0.4",
        "click_spinner==0.1.10",
    ],
    entry_points={"console_scripts": ["microsoftaca=cli:cli"]},
)
