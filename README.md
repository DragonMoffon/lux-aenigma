# Lux Aenigma

A short light-based puzzle game built with Python Arcade.

## Development

### General

Make sure you have Python 3.11+, but use 3.11 compat features if your editor has them.

### Setup

#### TL;DR

1. Make and create a venv:
   * If on Python 3.12+ and using PyCharm, create `.venv` from an external terminal
   * If your IDE / editor doesn't auto-create venvs, do whatever
2. `pip install -Ie .`
3. If you ignored the instructions, se next section


#### Python 3.12 Problems

TL;DR: Close PyCharm, delete `.venv`, `python3.12 -m venv .venv`

When do you do that? When you get something that looks like the output below.


```console
Collecting colored==1.4.2 (from digiformatter->Lux-Aenigma==26.3.2024a0)
  Downloading colored-1.4.2.tar.gz (56 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 56.7/56.7 kB 2.3 MB/s eta 0:00:00
  Preparing metadata (setup.py) ... error
  error: subprocess-exited-with-error
  
  × python setup.py egg_info did not run successfully.
  │ exit code: 1
  ╰─> [11 lines of output]
      Traceback (most recent call last):
        File "<string>", line 2, in <module>
        File "<pip-setuptools-caller>", line 14, in <module>
        File "/home/user/src/lux-aenigma/.venv/lib/python3.12/site-packages/setuptools/__init__.py", line 16, in <module>
          import setuptools.version
        File "/home/user/src/lux-aenigma/.venv/lib/python3.12/site-packages/setuptools/version.py", line 1, in <module>
          import pkg_resources
        File "/home/user/src/lux-aenigma/.venv/lib/python3.12/site-packages/pkg_resources/__init__.py", line 2191, in <module>
          register_finder(pkgutil.ImpImporter, find_on_path)
                          ^^^^^^^^^^^^^^^^^^^
      AttributeError: module 'pkgutil' has no attribute 'ImpImporter'. Did you mean: 'zipimporter'?
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
error: metadata-generation-failed

× Encountered error while generating package metadata.
╰─> See above for output.

```

Stuff I read to help fix this:

* [Inspiring but not directly clear blog post](https://pythontest.com/posts/2023/2023-10-02-py312-impimporter/)
* [Less useful StackOverflow thread](https://stackoverflow.com/questions/77364550/attributeerror-module-pkgutil-has-no-attribute-impimporter-did-you-mean)
