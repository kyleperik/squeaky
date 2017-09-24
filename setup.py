from setuptools import setup

setup(
    name='livecode',
    long_description=__doc__,
    packages=['livecode'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'python-socketio',
        'Flask',
        'eventlet',
        'redis',
    ]
)
