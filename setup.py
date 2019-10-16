from setuptools import setup

def read_readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='simple_gpu_scheduler',
    version='0.1.2',
    description='A simple scheduler for running commands on multiple GPUs.',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/ExpectationMax/simple_gpu_scheduler',
    author='Max Horn',
    author_email='maexlich@gmail.com',
    packages=['simple_gpu_scheduler'],
    python_requires='>3.6',
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    entry_points={
      'console_scripts': [
          'simple_gpu_scheduler=simple_gpu_scheduler.scheduler:main',
          'simple_hypersearch=simple_gpu_scheduler.hypersearch:generate_commands'
      ],
    },
    zip_safe=False
)
