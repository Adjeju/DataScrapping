from setuptools import setup, find_packages
setup(
    name="hotline",
    entry_points={'scrapy': ['settings = hotline.settings']},
    version="1.0.1",
    packages=find_packages(),
)