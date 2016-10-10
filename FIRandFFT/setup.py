import sys
from cx_Freeze import setup, Executable

#base = None
if sys.platform == "win32":
        base = "Win32GUI"#window only, no console

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "FIRandFFT",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]FIRandFFT.exe",            # Target
     None,                     # Arguments
     "yoshihara.yuusuke@gmail.com",                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]

msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data}


includes = ["PySide.QtCore", "PySide.QtGui", "gui2", "conf","pyqtgraph", "sys", "os", "wave", "FileDialog"]
excludes = ["tkinter", "PyQt4", "PyQt5", "mpl-data", "OpenGL", "cffi", "tornado", "mpl-data", "setuptools", "json", "email", "matplotlib",
"tcl", "tk", "cookielib", "mimetools", "mimetypes", "Tkinter"]
packages = ["numpy", "scipy"]


setup(
        name = "FIRandFFT",
        version = "1.0",
        author = "Yoshihara Yusuke",
        author_email = "yoshihara.yuusuke@gmail.com",
        url = "http://soft.sakuraweb.com/firandfft/",
        description = "FIR filtre on GUI",
        options = {"bdist_msi": bdist_msi_options, "build_exe": {"packages": packages,"includes": includes,"excludes": excludes}},
        executables = [Executable("gui1.py", base=base, icon="frame.ico", targetName="FIRandFFT.exe", shortcutName ='FIRandFFT', shortcutDir ="ProgramMenuFolder")],
)
#,"gio","importlib","stsci","pbr","ply","logging","gi","mock","pytz","pkg_resources","bsddb","glib","cairo","nose","gtk","multiprocessing","gobject","funcsigs","compiler","pycparser","PIL","xml","pysideuic","mpl_toolkits","tcl","tk"]
