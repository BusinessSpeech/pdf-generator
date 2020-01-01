import shutil


def create_zip(path):
    filename = 'trainings'
    file_ext = 'zip'
    shutil.make_archive(filename, file_ext, path)
    return filename + '.' + file_ext
