from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ['dns','dns.resolver','dns.rdatatype'],
                 'excludes': [],
                 'include_files': [('variables.env', 'variables.env')]
                 }

BASE = "gui"

executables = [
    Executable('wheel_of_luck.py', base=BASE)
]

setup(name='WheelOfLuck',
      version = '2.0.1',
      description = 'Interactive handler for Discord based solution of a game to play in a group',
      options = {
          'build_exe': build_options,
          'bdist_rpm': {
              'release': '1',  # Control the release number here
              'packager': 'Martin @R4tmax Kadlec kadlec.m.90@gmail.com',
          }
      },
      executables = executables)
