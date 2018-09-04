from setuptools import setup

setup(
    name='becca_toolbox',
    version='0.10.0',
    description='Some tools for working with Becca',
    url='http://github.com/brohrer/becca_toolbox',
    download_url='https://github.com/brohrer/becca_toolbox/archive/master.zip',
    author='Brandon Rohrer',
    author_email='brohrer@gmail.com',
    license='MIT',
    packages=['becca_toolbox'],
    include_package_data=True,
    install_requires=['becca'],
    zip_safe=False)
