from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ['dns','dns.resolver','dns.rdatatype'],
                 'excludes': [],
                 'include_files': [('variables.env', 'variables.env')]
                 }

base = "gui"

executables = [
    Executable('wheel_of_luck.py', base=base)
]

setup(name='WheelOfLuck',
      version = '2.0.1',
      description = 'Interactive handler for Discord based solution of a game to play in a group',
      options = {'build_exe': build_options},
      executables = executables)
