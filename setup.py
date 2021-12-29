from setuptools import setup, find_packages

setup(name='etl-py-drawio-datamapper',
      version='0.1',
      description='Datamapping generator for draw.io',
      url='http://github.com/vaytaliy/etl-py-drawio-datamapper',
      author='Vitaly Zhidkih',
      author_email='vitalyzhidkih@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['openpyxl==3.0.9', 'et-xmlfile==1.1.0'],
      zip_safe=False)