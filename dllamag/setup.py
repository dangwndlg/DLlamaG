from setuptools import setup, find_packages

# Define the name and version of your package
package_name = "dllamag"
package_version = "1.0.0"

# Package description
package_description = "DLG's newest chatbot"

# Package author and contact information
package_author = "Dan Gawne"
package_author_email = "dangawne@outlook.com"

# Define the packages to include (find_packages will discover them automatically)
packages = find_packages()

# Define package dependencies (including requests)
install_requires = [
    "requests",  # Add requests as a requirement
    # List any other dependencies your module may need
]

setup(
    name=package_name,
    version=package_version,
    description=package_description,
    author=package_author,
    author_email=package_author_email,
    packages=packages,
    install_requires=install_requires,
    # Add any additional metadata here, e.g., project URL, license, keywords, classifiers, etc.
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
