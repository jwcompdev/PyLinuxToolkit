import setuptools

setuptools.setup(
    name="pylinuxtoolkit-jwcompdev",
    version="0.0.1",
    author="JWCompDev",
    author_email="jwcompdev@gmail.com",
    description="A gui application for linux administration.",
    # long_description = file: README.md
    # long_description_content_type = text/markdown
    url="https://github.com/jwcompdev/PyLinuxToolkit",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
)
