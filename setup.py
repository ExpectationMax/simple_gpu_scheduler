from setuptools import setup

setup(
    name='simple_gpu_scheduler',
    version='0.1',
    description='A simple scheduler for running commands on multiple GPUs.',
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
          'simple_gpu_scheduler=simple_gpu_scheduler.command_line:main'],
    },
    zip_safe=False
)
