from setuptools import find_packages, setup


def get_readme():
    with open('README.md', encoding='utf-8') as readme:
        content = readme.read()
    return content


if __name__ == '__main__':
    setup(
        name='tracklet_parser',
        version='1.0.0',
        description='A parser for tracklet labels created by the Computer'
        'Vision Annotation Tool (CVAT).',
        long_description=get_readme(),
        author='Bjoern Holtvogt',
        author_email='bjoern.holtvogt@gmail.com',
        keywords='tracklet, cvat, kitti',
        url='https://github.com/holtvogt/tracklet_parser',
        packages=find_packages(),
        license='MIT License',
        setup_requires=['cython', 'numpy'],
        install_requires=[
            'black',
            'codespell',
            'docformatter',
            'isort',
            'pandas',
            'pre-commit',
        ],
    )
