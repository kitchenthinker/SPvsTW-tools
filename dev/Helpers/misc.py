import os


def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def get_files_path(start_folder_path: str, deep: int = 0) -> dict[str:str]:
    paths_list = dict()
    for dirpath, dirname, filenames in walklevel(start_folder_path, deep):
        for filename in filenames:
            paths_list[filename] = (os.path.join(dirpath, filename))
    return paths_list