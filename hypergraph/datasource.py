from zipfile import ZipFile
from os import path, remove
import shutil

class Datasource:
    """Provides methods to manipulate a Tableau packaged datasource file
    
    Args:
        file_path: Path to the packaged datasource file (.tdsx)
    """
    def __init__(self, file_path):
        self.path = file_path
    
    def replace_extract(self, file_path):
        """Replace Hyper file in Tableau Packaged Datasource
        
        Args:
            file_path: Path to the replacement hyper file.
        """
        tmp_file = shutil.copy2(self.path, "tmpzip")
        with ZipFile(tmp_file) as src, ZipFile(self.path, "w") as dst:
            for src_info in src.infolist():
                _, src_tail = path.split(src_info.filename)
                _, file_tail = path.split(file_path)
                if src_tail == file_tail:
                    dst.write(file_path, src_info.filename)
                else:
                    with src.open(src_info) as src_file:
                        dst.writestr(src_info, src_file.read())

        remove(tmp_file)
