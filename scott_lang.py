import os
import struct
import csv
import argparse


parser = argparse.ArgumentParser(description="Scott Pilgrim Language Packer")
parser.add_argument('-wnums', help="add numbers to text", type=int, choices=[1, 0], default=0)
parser.add_argument('-wrus', help="get original text or translated numbers to text", type=int, choices=[1, 0], default=0)


def get_files_path(start_folder_path: str) -> dict[str:str]:
    paths_list = dict()
    for dirpath, dirname, filenames in os.walk(start_folder_path):
        for filename in filenames:
            paths_list[filename] = (os.path.join(dirpath, filename))
    return paths_list


if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    with_nums = args.wnums
    with_tr = args.wrus
    byte_splitter = b'\x00\x00'

    rus_ = {}
    with open('files\\lang\\tr.csv', mode='r', encoding='utf8') as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            rus_[int(rows['index'])] = {
                'index': rows['inner_index'],
                'text': rows['rus'] if with_tr else rows['eng'],
            }
    
    with open('files\\lang\\english.bof.org', mode='rb') as loc_file, open('files\\lang\\english.bof', mode='wb') as mod_file:

        # write header
        mod_file.write(loc_file.read(4))
        # write total lines
        mod_file.write(loc_file.read(4))

        # get length of data * 2 'cause unicode encoding
        data_length = int.from_bytes(loc_file.read(4), byteorder="little") * 2
        main_data = loc_file.read(data_length)

        splitted_data = main_data.rsplit(sep=byte_splitter)

        new_data = b''

        for i, row in enumerate(splitted_data[:-1]):

            mod_data = rus_.get(i, None)
            if mod_data is None:
                w_data = row
            else:
                if mod_data['text'].strip() == '':
                    w_data = row
                else:
                    w_data = mod_data['text'].strip().replace('<lf>', '\n').encode('utf-16-le')

                if with_nums:
                    w_data = mod_data['index'].encode('utf-16-le') + b'\x20\x00' + w_data

            lw_data = len(w_data)
            new_data += w_data + b'\x00\x00'
        
        mod_file.write(struct.pack('<I', len(new_data)//2))
        mod_file.write(new_data)
        mod_file.write(loc_file.read())

