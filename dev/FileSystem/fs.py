
from dataclasses import dataclass, field, asdict
from struct import pack, unpack
from dev.FileSystem.gdf import GameDataFile
from dev.Logs.logger import log
import dev.Helpers.misc as misc

import zlib
import io
import json
import os
import pickle


GAMEDATA_FSNAME = 'gamedata.fat'
GAMEDATA_DNAME = 'gamedata'
FILESPATH = 'files'


@dataclass
class GameDataFatEntry:

    id: int
    offset: int
    zsize: int = 128


class GameDataFat:

    @staticmethod
    def is_compressed(f2b: bytes) -> bool:
        return f2b == b'\x78\xDA'
    
    def is_data_loaded(self) -> bool:
        return self.entries_count > 0

    def __get_bytestream(self):
        with open(self.path_to_file, mode='rb') as fBuffer:
            f2b = fBuffer.read(2)
            fBuffer.seek(0)
            compressed = GameDataFat.is_compressed(f2b)
            fResult = zlib.decompress(fBuffer) if compressed else fBuffer.read()
            return io.BytesIO(fResult)
           
    def __read_file(self):
        fBuffer = self.__get_bytestream()
        self.entries_count = unpack('<I', fBuffer.read(4))[0]

        for i in range(self.entries_count):
            entry_id, entry_offset, _ = unpack('<3I', fBuffer.read(12))
            newEntry = GameDataFatEntry(entry_id, entry_offset)
            self.entries.append(newEntry)
            # get_prev_size
            if 0 < i < self.entries_count:
                prevEntrie = self.entries[i - 1]
                prevEntrie.zsize = newEntry.offset - prevEntrie.offset
        del fBuffer

    def save_to_file(self):
        log.info(f'Prepare json for saving.')
        entries = {item.id: asdict(item) for item in self.entries}
        js = {
            "entries_count": self.entries_count,
            "entries": entries,
        }
        log.info(f'Preparing is done.')
        log.info('Saving json file...')
        NEW_FILE = os.path.join(FILESPATH, "out", 'GameDataFat.json')
        with open(NEW_FILE, mode='w', encoding='utf-8') as f:
            json.dump(js, f, indent=2, ensure_ascii=False)
            log.info(f"Json file of {GAMEDATA_FSNAME} file structure has been saved.")

    def recreate_fat(self, compress_after: bool = True):
        
        if not self.is_data_loaded():
            log.info("Nothing to recreate. Data is empty.") 
            return     
        
        log.info("Prepare bytes for saving")

        fat_bytes = io.BytesIO()
        fat_bytes.write(pack('<I', self.entries_count))
        for entry in self.entries:
            fat_bytes.write(pack('<3I', *(entry.id, entry.offset, 0)))
        fat_bytes.write(pack('<I', 0))

        if compress_after:
            log.info('Compress new fat file.')
            fat_bytes = io.BytesIO(zlib.compress(fat_bytes.getbuffer(), 9))
        
        log.info('Start writing new fat file.')
        NEW_FILE = os.path.join(FILESPATH, "out", GAMEDATA_FSNAME)
        with open(NEW_FILE, mode="wb") as new_fat:
            # write entries counter
            new_fat.write(fat_bytes.getbuffer())
        log.info('End writing new fat file.')
        del fat_bytes

    def read_data(self):
        self.__read_file()

    def recalculate_offsets(self):
        pos_offset = 0
        for entry in self.entries:
            entry.offset = pos_offset
            pos_offset += entry.zsize

    def __init__(self, path_to_file: str):
        self.path_to_file = os.path.join(path_to_file, GAMEDATA_FSNAME)
        self.entries_count: int = 0
        self.entries: list[GameDataFatEntry] = []


@dataclass
class GameDataManager:

    # gamedata filesystem
    path_to_files: str
    records: int = 0
    gd_fsystem: GameDataFat | None = None
    gd_data: list[GameDataFile] | None = field(default_factory=list)
    hash_map: dict = field(default_factory=dict)

    def initialize(self):
        self.gd_fsystem_init()
        self.gd_data_init()
        self.save_to_pickle()

    def gd_fsystem_init(self):
        self.gd_fsystem = GameDataFat(self.path_to_files)
        self.gd_fsystem.read_data()
        # temp
        if self.records == 0: self.gd_fsystem.entries_count

    def __get_gd_data_bytes(self):
        path_to_data = os.path.join(self.path_to_files, GAMEDATA_DNAME)
        with open(path_to_data, mode='rb') as f:
            return io.BytesIO(f.read())
    
    def __mark_modified(self):
        MODS_FOLDER = os.path.join(FILESPATH, "mods")

        raw_list_of_mods = misc.get_files_path(MODS_FOLDER, 3)
        print(raw_list_of_mods)
        mods = {}
        
        def int_chk(itm):
            try:
                result = int(itm)
            except ValueError:
                result = -1
            return result
            
        for file, filepath in raw_list_of_mods.items():
            file_id, file_chunk, *trash = map(int_chk, file.split('.')[0].split('_'))

            if mods.get(file_id, None) is None:
                mods[file_id] = [(file_chunk, filepath)]
            else:
                mods[file_id].append((file_chunk, filepath))
        
        for id, chunks in mods.items():
            gdf_index = self.hash_map[id]
            game_file: GameDataFile = self.gd_data[gdf_index]
            for chk in chunks:
                game_file_chunk = game_file.chunks[chk[0]]
                game_file_chunk.modified = True
                game_file_chunk.mod_path = chk[1]
            game_file.modified = True

    def save_to_pickle(self):
        path_to_save = os.path.join(FILESPATH, 'source', 'data.pickle')
        with open(path_to_save, mode='wb') as pickle_file:
            pickle.dump(self, pickle_file)

    def gd_data_init(self):

        if self.gd_fsystem is None:
            self.gd_data_init(self.path_to_files)

        gdBuffer = self.__get_gd_data_bytes()
        for index, fs_entry in enumerate(self.gd_fsystem.entries, start=1):
            if self.records != 0 and index > self.records: break

            zchunk = gdBuffer.read(fs_entry.zsize)

            newGDF = GameDataFile(
                id=fs_entry.id,
                raw_data=zchunk,
            )

            log.info(f"Add entry id={fs_entry.id} to gamedata.")
            log.info(f"Finish {index} of {self.gd_fsystem.entries_count} \n")
            self.gd_data.append(newGDF)
            self.hash_map[newGDF.id] = index - 1
    
    def pack(self):
        # TODO: Check for modified files.
        self.__mark_modified()

        new_gdata_filepath = os.path.join(FILESPATH, 'out', GAMEDATA_DNAME)
        fFat = self.gd_fsystem
        fData: list[GameDataFile] = self.gd_data
        with open(new_gdata_filepath, mode='wb') as ngd:
            for index, (item_fat, item_data) in enumerate(zip(fFat.entries, fData), start=1):
                if item_data.modified:
                    item_data.import_mod()
                new_data = item_data.recreate_data()
                # TODO delete after checking
                #if item_data.modified:
                #   with open(f'modz\\{index}.raw', mode='wb') as modfile:
                #       modfile.write(zlib.decompress(new_data))
                ###
                item_fat.zsize = len(new_data)
                ngd.write(new_data)
                log.info(f"Write chunk: {item_fat.id} - {index} of {fFat.entries_count}.")
        fFat.recalculate_offsets()
        fFat.recreate_fat(compress_after=True)

    def extract_raw(self):

        fData = self.gd_data
        for item_data in fData:
            if not item_data.empty:
                new_data = item_data.recreate_data()
                ngd_item_path = os.path.join(FILESPATH, 'raw', f'{item_data.id}')
                with open(ngd_item_path, mode='wb') as ef:
                    ef.write(zlib.decompress(new_data))
                    log.info(f"Write file: {item_data.id}.")
