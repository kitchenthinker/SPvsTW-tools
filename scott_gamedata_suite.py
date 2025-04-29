import argparse
import dev.FileSystem.fs as fsystem
import pickle
import os

parser = argparse.ArgumentParser(description="Scott Pilgrim GameData Suite")
parser.add_argument('mode', help="import or export", choices=['import', 'export'])

if __name__ == "__main__":
    args = parser.parse_args()
    path2file = 'files\\source'

    data_pickle_path = os.path.join(path2file, 'data.pickle')
    if os.path.exists(data_pickle_path):
        with open(data_pickle_path, mode='rb') as file_pickle:
            newFat = pickle.load(file_pickle)
    else:
        newFat = fsystem.GameDataManager(path2file, 0)


    if args.mode == 'export':
        newFat.initialize()
    elif args.mode == 'import':
        newFat.pack()
    else:
        print("Command does not exist"