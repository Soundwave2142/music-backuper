import os
import src.components.filesystem_helper as fh


# TODO: Rework this class
class ComponentProcessorCleaner:

    def process(self, directory):
        for folder in os.listdir(directory):
            sub_directory = os.path.join(directory, folder)
            if os.path.isdir(sub_directory):
                if self.auto_delete(folder):
                    answer = 'y'
                    print("Auto >> DELETING >>>>  %s  <<<<   " % folder)
                elif self.auto_skip(folder):
                    answer = 'n'
                    print("Auto >> SKIPPING >>>>  %s  <<<<   " % folder)
                else:
                    answer = input("Has folder >>>>  %s  <<<<, DELETE? Enter for skip, 'y' for yes: " % folder)

                if answer.lower() == 'y':
                    fh.delete(sub_directory)

    def auto_delete(self, folder):
        auto_delete = ["Covers", "Cover", "Artwork", "Scans"]
        for text in auto_delete:
            if folder.lower().startswith(text.lower()):
                return True

        return False

    def auto_skip(self, folder):
        autoskip = ["Disc 1", "Disc 2", "Disc 3", "CD1", "CD2", "CD3", "CD 1", "CD 2", "CD 3"]
        for text in autoskip:
            if folder.lower().startswith(text.lower()):
                return True

        return False
