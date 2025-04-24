from setuptools import setup, find_packages

setup(
    name='image_app',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'ImageApp=image_app.cli:main',
        ]
    },
)
