# Tools

Various tools used in the project.

## Tool to check Python version

```check_python_version.py```

Check if the installed Python interpreter has correct version.

This script has to be called with two command line arguments:
expected_major_version expected_minor_version

The script then check if actual Python version (major+minor) is
the same or newer than expected version.

Usage:
python check_python_version.py 2.7
python3 check_python_version.py 3.6
python3 check_python_version.py 3.7
etc.
