from setuptools import setup, find_packages
from setuptools.command.install import install as _install

def readme():
    with open('README.rst') as f:
        return f.read()

class Install(_install):
    def run(self):
        _install.do_egg_install(self)
        import nltk
        nltk.download()

setup(
      name='jobscrapper-etl',
      version='0.1',
      description='Scrap job posting, get a list of top words and import job details into MySQL database.',
      long_description=readme(),
      classifiers=[
        'Development Status :: 2 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
      ],
      keywords='ETL data pipeline database import',
      url='http://github.com/mdauthentic/jobscrapper-etl',
      author='Muideen Lawal',
      author_email='muideen.lawal320@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
            'Selenium',
            'nltk',
            'Pandas',
            'SQLAlchemy',
            'PyMySQL',
      ],
      setup_requires=['nltk'],
      cmdclass={'install': Install},
      include_package_data=True,
      entry_points={
        'console_scripts': [
            'run = main:main',
        ],
      },
      zip_safe=False
    )