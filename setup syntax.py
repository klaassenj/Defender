__author__ = 'Jason'


import cx_Freeze

pyfiles = [cx_Freeze.Executable("Main.py")]

cx_Freeze.setup(
    name = "Title",
    options = {
                        "build_exe": {"packages": ["pygame"], "included files": ["file1", "file2", "file3..."]}
                    },
    description = "Description",
    executables = pyfiles
)

# CMD -->