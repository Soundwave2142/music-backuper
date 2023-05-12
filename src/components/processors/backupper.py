import os
import shutil
import src.components.filesystem_helper as fh


# TODO: Rework this class
class ComponentProcessorBackupper:
    root_dir = os.getcwd()
    copy_to_dir = 'E:\\Music'

    def process(self, directory):
        copy_dir = directory.replace(self.root_dir, self.copy_to_dir)
        if os.path.exists(copy_dir):
            if fh.get_dir_size(directory) == fh.get_dir_size(copy_dir):
                return
            fh.delete(copy_dir, True)

        shutil.copytree(directory, copy_dir)
