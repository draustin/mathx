from setuptools import setup, find_packages

setup(name="mathx",
      version=0.1,
      description="Mathematics extensions",
      author='Dane Austin',
      author_email='dane_austin@fastmail.com.au',
      url='https://github.com/draustin/mathx',
      license='BSD',
      packages=find_packages(),
      install_requires=['numpy'],
      test_requires=['pytest'])
