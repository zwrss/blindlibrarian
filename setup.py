from setuptools import setup

setup(
      name='blindlibrarian',
      version='0.1.0',
      description='Command line librarian for movies and TV shows.',
      url='https://github.com/zwrss/blindlibrarian',
      author='Pawel Mlynarczyk',
      author_email='zwarios@gmail.com',
      license='MIT',
      packages=['blindlibrarian'],
      entry_points={
               'console_scripts': ['blindlibrarian=blindlibrarian:main'],
           },
      install_requires=[
          'guessit',
          'requests',
          'docopt'
      ],
      keywords=[
           'movies', 'TV', 'TV-series'
      ],
      classifiers=[
          'Environment :: Console',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.8',
          'Topic :: Utilities',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
)