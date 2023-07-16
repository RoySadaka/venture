import os
from setuptools import setup, find_packages
from io import open as io_open

src_dir = os.path.abspath(os.path.dirname(__file__))

install_requires = []

path_requirements_dev = os.path.join(src_dir, 'requirements-dev.txt')
for path in [path_requirements_dev]:
    with io_open(path, mode='r') as fd:
        for i in fd.read().strip().split('\n'):
            req = i.strip().split('#', 1)[0].strip()
            install_requires.append(req)


README_md = ''
fndoc = os.path.join(src_dir, 'README.md')
with io_open(fndoc, mode='r', encoding='utf-8') as fd:
    README_md = fd.read()


classifiers=[
        # (https://pypi.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Utilities'
    ]

setup(
    name='venture-ai',
    version='0.9.6',
    description='A Fast, Flexible Trainer with Callbacks and Extensions for PyTorch',
    long_description_content_type='text/markdown',
    long_description=README_md,
    license='MIT Licences',
    url='https://github.com/roysadaka/venture',
    author='Roy Sadaka',
    maintainer='lpd developers',
    maintainer_email='torch.lpd@gmail.com',
    packages=find_packages(exclude=['tests', 'tests/*', 'examples', 'examples/*']),
    install_requires=install_requires,
    python_requires='>=3.9',
    classifiers=classifiers,
    keywords=['ai,natural language processing,large language models,project exploration,chatbot,documentation exploration,reasoning based search,assistant,chatgpt,openai']
)