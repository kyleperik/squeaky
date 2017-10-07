from setuptools import setup

setup(
    name='squeaky',
    long_description=__doc__,
    packages=['squeaky'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'python-socketio',
        'Flask',
        'eventlet',
        'redis',
    ]
)
