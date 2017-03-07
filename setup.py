from setuptools import setup

setup(name='lineman',
      version='0.0.1',
      description='Lineman fixes data problems that will keep your data from going into redcap.',
      url='http://github.com/pfwhite/lineman',
      author='Patrick White',
      author_email='pfwhite9@gmail.com',
      license='MIT',
      packages=['lineman'],
      entry_points={
          'console_scripts': [
              'lineman = lineman.__main__:main',
          ],
      },
      install_requires=['cappy', 'docopt', 'pyyaml', 'python-dateutil'],
      zip_safe=False)
