import shutil
import os


def copyFile(source_path, destination_path, exist_ok):
    if (os.path.isfile(destination_path) and exist_ok):
        return 
    shutil.copy2(source_path, destination_path)

def getRelativePath(path, fromPath):
    fromPath = os.path.split(fromPath)[0]
    return os.path.relpath(path, start=fromPath)

def run_command(path, command):
    return os.system(f"cd {path} && {command}")

def version_path_ok(version_name):
    return version_name.replace('/','_')