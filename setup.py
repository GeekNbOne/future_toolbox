from setuptools import setup

setup(name='future_toolbox',
      version='1.1.4',
      description='Toolbox to manipulate future information',
      author='Luc Berthiaume',
      author_email='luc.berthiaume@innocap.com',
      license='Innocap',
      packages=['fut_maturity'],
      include_package_data=True,
      install_requires=['dateutils'],
      zip_safe=False)
