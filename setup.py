from setuptools import setup, find_packages


setup(
    name='rnkfinder',
    version='0.0.1',
    description="",
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/BobsBibs/rnkfinder',
    author='Elizabeth S.',
    author_email='hitomi.t@ya.ru',
    license='MIT License',
    packages=find_packages(),
    setup_requires=['setuptools_scm'],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "rnkfinder = rnkfinder.main:cli",
        ],
    },
    install_requires=open('requirements.txt').read().splitlines(),
)