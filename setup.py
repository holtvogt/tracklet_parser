from setuptools import find_packages, setup


def get_readme() -> str:
    """Get README.md content.

    Returns:
        content (str): The README.md content
    """

    with open("README.md", encoding="utf-8") as readme:
        content = readme.read()
    return content


if __name__ == "__main__":
    setup(
        name="tracklet_parser",
        version="1.0.0",
        description=(
            "A parser for tracklet labels in KITTI Raw Format 1.0 created by"
            " the Computer Vision Annotation Tool (CVAT)."
        ),
        long_description=get_readme(),
        author="Bjoern Holtvogt",
        author_email="bjoern.holtvogt@gmail.com",
        keywords="tracklet, cvat, kitti, annotation",
        url="https://github.com/holtvogt/tracklet_parser",
        packages=find_packages(),
        license="MIT License",
        python_requires=">=3.9",
        install_requires=[
            "black",
            "codespell",
            "docformatter",
            "isort",
            "numpy",
            "pandas",
            "pre-commit",
            "pylint",
        ],
    )
