import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
# with open(os.path.join(here, 'CHANGES.txt')) as f:
#    CHANGES = f.read()
CHANGES = ''

requires = [
    'pyramid',
]

setup(name='{{cookiecutter.project_name}}',
      version='0.0',
      description='{{cookiecutter.project_name}}',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="{{cookiecutter.project_name}}",
      entry_points="""\
      [pyramid.scaffold]
      module = scaffolds:ModuleProjectTemplate
      init_starter3 = scaffolds:InitStarter3ProjectTemplate
      pkg = scaffolds:PkgProjectTemplate
      """,
      )
