import cx_Freeze
executables = [cx_Freeze.Executable("Game.py")]

cx_Freeze.setup(name="Marc",option={"build_exe" : {"package" : ["pygame"], "include_files": ["res"]}}, executables=executables)
