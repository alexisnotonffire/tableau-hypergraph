from zipfile import ZipFile
from os import path, remove
import shutil

TDSX = "resources/hypergraph.tdsx"
FILE = "tableau.hyper"
BUILD_DIR = "build"

class Datasource:
    def __init__(self, file_path):
        self.path = file_path
    
    def replace_hyper(self, file_path):
        tmp_file = shutil.copy2(file_path, "tmpzip")
        with ZipFile(tmp_file) as src, ZipFile(self.path, "w") as dst:
            for src_info in src.infolist():
                _, tail = path.split(src_info.filename)
                if tail == FILE:
                    dst.write(f"{BUILD_DIR}/{FILE}", src_info.filename)
                else:
                    with src.open(src_info) as src_file:
                        dst.writestr(src_info, src_file.read())

        remove(tmp_file)
            


ds = Datasource(TDSX)
ds.replace_hyper("test")