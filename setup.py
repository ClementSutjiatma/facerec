from setuptools import setup

setup(
    name='facerec',
    packages=['facerec'],
    include_package_data=True,
    install_requires=[
        'flask',
        'face_recognition'
    ],
)
