from os import listdir
from os.path import isfile, join

class Files:

    def __init__(self, path):
        self.path = path

    def get_numeric_files(self):
        files = self.get_files()
        dictionary = {}
        for file in files:
            file_name = file.split(".")[0]
            try:
                file_int = int(file_name)
                dictionary[file_int] = file
            except:
                # File wasn't an image file
                continue

        output = []
        for i in sorted(dictionary.keys()):
            # Add empty strings if we have future higher numbers
            while i != len(output):
                output.append("")

            output.append(dictionary[i])

        return output

    def get_files(self):
        return [f for f in listdir(self.path) if isfile(join(self.path, f))]
