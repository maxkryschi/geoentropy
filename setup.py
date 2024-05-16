from setuptools import setup, find_packages

setup(
    name='GeoEntropy',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'matplotlib', 'scipy', 'shapely'],
    include_package_data=True,
    description='A Python package for computing geometric/spatial entropy metrics for data in matrix format.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/maxkryschi/geoentropy',
    author='Max Kryschi',
    author_email='',
    license='MIT License',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
