from setuptools import setup, find_packages

packages = find_packages()
package_author = "Dan Gawne"
package_author_email = "dangawne@outlook.com"
package_description = "DLG's newest chatbot"
package_name = "dllamag"
package_version = "1.0.0"

install_requires = [
    "requests",  
    "pydantic"
]

setup(
    name=package_name,
    version=package_version,
    description=package_description,
    author=package_author,
    author_email=package_author_email,
    packages=packages,
    install_requires=install_requires,
    url="https://github.com/dangwndlg/DLlamaG",
    license="",
    keywords="",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: License Name",
        "Programming Language :: Python :: 3",
    ],
)
