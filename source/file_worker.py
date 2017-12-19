import os


class FileWorker:
    def save_file(self, directory, file):
        path = os.path.join(directory, file.filename)
        with open(path, 'wb') as f:
            f.write(file.content)


class File:
    def __init__(self, file_path):
        self.filename = self.extract_name(file_path)
        self.content = self.read_file(file_path)

    @staticmethod
    def read_file(file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
        return content

    @staticmethod
    def extract_name(file_path):
        return os.path.split(file_path)[1]
