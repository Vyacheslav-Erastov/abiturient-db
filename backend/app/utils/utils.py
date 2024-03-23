import os
import shutil
from uuid import UUID
import zipfile

from fastapi import UploadFile

from app.core.config import settings


def extract_files(file_objects: list[UploadFile], task_id: UUID):
    dest_dir = os.path.join(settings.INPUT_PATH, str(task_id))
    output_dir = os.path.join(settings.OUTPUT_PATH, str(task_id))
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    try:
        for file_obj in file_objects:
            if zipfile.is_zipfile(file_obj.file):
                try:
                    zfile = zipfile.ZipFile(file_obj)
                    for filename in zfile.namelist():
                        ext = os.path.splitext(os.path.basename(filename))[1]
                        # if (ext_filter and ext == ext_filter) or (ext_filter == ''):
                        #     zfile.extract(filename, dest_dir)
                        print(ext)
                except zipfile.BadZipfile:
                    pass
            elif file_obj.filename.endswith(".mp4"):
                with open(os.path.join(dest_dir, file_obj.filename), "wb") as f:
                    f.write(file_obj.file.read())
                # shutil.copy(file_obj.file.read(), os.path.join(dest_dir, file_obj.filename))
    except Exception as e:
        os.rmdir(dest_dir)
        raise e
    return dest_dir
