# PyDarts

Python binding of Darts

## Installation

```
$ pip install pydarts
```

## Usage

``` python

from pydarts import PyDarts

# build dictionary
da = PyDarts(["py", "python", "cpp"])  # create dict

# search keys in dict
da.search("python cpp")  # => [("python", 1), ("cpp", 1)]

# search any key in dict
da.search("python cpp", longest=False)  # => [("py", 1), ("python", 1), ("cpp", 1)]

# save dict
da.save("/path/to/save.da")

# load dict from file
da = PyDarts.load("/path/to/save.da")
```
