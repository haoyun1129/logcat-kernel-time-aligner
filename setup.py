import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='logcat-kernel-time-aligner',  
    version='0.1',
    scripts=['logcat-kernel-time-aligner'] ,
    author="haoyun.tw",
    author_email="haoyun.tw@gmail.com",
    description="Align the kernel timestamps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yinhaoyun/logcat-kernel-time-aligner/",
    packages=setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

