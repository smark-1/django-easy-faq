from distutils.core import setup
setup(
      packages = ['faq'],
      include_package_data = True,
      name = 'django-easy-faq',         # How you named your package folder (MyLib)

      version = '1.2',      # Start with a small number and increase it with every change you make
      license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
      author = 'dragoncommits',                   # Type in your name
      url = 'https://github.com/dragoncommits/django-easy-faq/',   # Provide either the link to your github or to your website
      download_url = 'https://github.com/dragoncommits/django-easy-faq/archive/refs/tags/1.1.tar.gz',
      keywords = ['django', 'FAQ', 'django-easy-faq','simple','frequently asked questions'],   # Keywords that define your package best
      install_requires=[            # I get to this in a second
              'django',
          ],
      classifiers=[
        'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which python versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],

)