try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Naive modern search using Freebase API',
    'author': 'Marshall Shen',
    'url': 'github.com/marshallshen',
    'download_url': 'Where to download it.',
    'author_email': 'shen.marshall@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['app'],
    'scripts': [],
    'name': 'naive-modern-search'
}

setup(**config)