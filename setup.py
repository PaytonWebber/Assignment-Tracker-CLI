from setuptools import setup, find_packages

setup(
    name="assignment_tracker",
    version="0.0.2",
    description="The Assignment Tracker CLI Tool is a Python-based command line interface designed to efficiently interact with a CSV file containing assignment details.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="Payton Webber",
    author_email="paytonwebber@gmail.com",
    url="https://github.com/PaytonWebber/Assignment-Tracker-CLI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
        package_data={
        '': ['assignment_tracker_config.ini'],
    },
    install_requires=[
        "rich==13.5.2",
        "typer==0.9.0",
        "typing_extensions==4.7.1"
    ],
    entry_points={
        "console_scripts": [
            "assignment-tracker=assignment_tracker.main:app"
        ]
    }
)
