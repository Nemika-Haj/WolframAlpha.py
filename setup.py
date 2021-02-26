from setuptools import setup

with open("README.md", "r") as f:
  readme = f.read()

setup(
  name = 'WolframAlpha.py',
  packages = ['wolfram'],
  version = '1.1.0',
  license='MIT',
  description = 'A WolframAlpha API Wrapper for Python.',
  author = 'Nemika',
  author_email = 'nemika@bytestobits.dev',
  url = 'https://github.com/Nemika-Haj/WolframAlpha.py',
  keywords = ["wolfram", "wolframalpha", "wolfram.py", "wolframalpha.py", "wrapper"],
  long_description=readme,
  long_description_content_type="text/markdown",
  install_requires=[
          'requests',
          'aiohttp',
          'asyncio'
      ],
  classifiers=[
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)