import os

max_size = 1024 * 1024 * 10  # 12 MB
allowed_extensions = {"jpg", "png", "jpeg", "gif"}


def allowed_file_extension(filename):
    extension = filename.rsplit(".")[1].lower()
    return "." in filename and extension in allowed_extensions


def allowed_file_size(file):
    start_position = file.tell()
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(start_position)
    return file_size <= max_size
