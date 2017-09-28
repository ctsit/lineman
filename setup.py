from setuptools import setup

#bring in __version__ from sourcecode
#per https://stackoverflow.com/a/17626524
#and https://stackoverflow.com/a/2073599

with open('lineman/version.py') as ver:
    exec(ver.read())

setup(name='lineman',
      version=__version__,
      description='Lineman fixes data problems that will keep your data from going into redcap.',
      url='http://github.com/ctsit/lineman',
      author='Patrick White',
      author_email='pfwhite9@gmail.com',
      license='Apache License 2.0',
      packages=['lineman'],
      entry_points={
          'console_scripts': [
              'lineman = lineman.__main__:cli_run',
          ],
      },
      install_requires=['cappy==1.1.1',
                        'docopt==0.6.2',
                        'pyyaml==3.12',
                        'python-dateutil==2.6.1'],
      dependency_links=["git+https://github.com/ctsit/cappy@1.1.1#egg=cappy-1.1.1"],
      zip_safe=False)
