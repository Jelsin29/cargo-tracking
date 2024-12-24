from setuptools import setup, find_packages

setup(
    name="cargo-tracking",
    version="1.0.0",
    author="Jelsin29",
    description="Online Cargo Tracking System",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=['astroid==3.3.6', 'black==24.10.0', 'click==8.1.8', 'coverage==7.6.9', 'dill==0.3.9', 'iniconfig==2.0.0', 'isort==5.13.2', 'mccabe==0.7.0', 'mypy-extensions==1.0.0', 'packaging==24.2', 'pathspec==0.12.1', 'platformdirs==4.3.6', 'pluggy==1.5.0', 'pylint==3.3.2', 'PyQt5==5.15.11', 'PyQt5-Qt5==5.15.16', 'PyQt5_sip==12.16.1', 'pytest==8.3.4', 'pytest-cov==6.0.0', 'python-dateutil==2.9.0.post0', 'setuptools==75.6.0', 'six==1.17.0', 'tomlkit==0.13.2', 'typing_extensions==4.12.2'],
    python_requires=">=3.13",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "cargo-tracking=src.main:main",
            "cargo-tracking-gui=src.gui_main:main",
        ],
    },
)
