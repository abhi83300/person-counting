from setuptools import setup, find_packages

setup(
    name="people-counter",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "numpy",
        "pyautogui",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple tool to count people on a computer screen",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/people-counter",
)