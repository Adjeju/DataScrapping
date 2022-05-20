from setuptools import setup, find_packages
setup(
 name="moyo",
 entry_points={'scrapy': ['settings = moyo.settings']},
 version="1.0.1",
 packages=find_packages(),
)