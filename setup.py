from setuptools import setup, Extension

try:
    from Cython.Build import cythonize
except ImportError:
    ext_modules = [
        Extension('pydarts', sources=['pydarts.cpp'])
    ]
else:
    ext_modules = cythonize(['pydarts.pyx'])

setup(
    name="pydarts",
    version="1.1.2",
    description="Python binding of Darts",
    author="JX PRESS Corp.",
    author_email="info@jxpress.net",
    url="https://github.com/jxpress/pydarts",
    include_package_data=True,
    ext_modules=ext_modules,
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ]
)
