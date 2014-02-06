from setuptools import setup

requirements = ['ciscoconfparse']

classifiers = ['Intended Audience :: Developers',
               'Intended Audience :: System Administrators',
               'License :: OSI Approved :: BSD License',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 2.7',
               'Topic :: Communications',
               'Topic :: Internet',
               'Topic :: Software Development :: Libraries',
               'Topic :: Software Development :: Libraries :: Python Modules',
               'Topic :: System :: Networking',
               'Topic :: System :: Systems Administration']

setup(name='pyiosdevice',
      version='0.1',
      description='Library for represening a subset of a Cisco config in a class',
      long_description=open('README.md').read(),
      author='Scott T. O\'Brien',
      author_email='scott@scottyob.com',
      url='https://github.com/scottyob/pyiosdevice',
      packages=['iosdevice'],
      package_data={'': ['README.md']},
      include_package_data=True,
      install_requires=requirements,
      license=open('LICENSE').read(),
      classifiers=classifiers,
      zip_safe=True)
