from dataclasses import dataclass, field, asdict
from struct import pack, calcsize, unpack
from io import BytesIO
from os import path
from json import dump
from enum import Enum, auto
from PIL import Image
from dev.Logs.logger import log
from dev.FileSystem.chunks.chunk import GameDataFileChunk


import zlib


class GraphicFormat(Enum):

    RGBA = 21
    UKNOWN = auto()

    def get_type(value):
        try:
            _type = GraphicFormat(value)
            return _type, value
        except ValueError:
            return GraphicFormat.UKNOWN, value

@dataclass
class Chunk_Graphic(GameDataFileChunk):
    # if solid then add uint [1] before

    dsize: int = field(init=False, default=0)
    ###
    width: int = field(init=False, default=0)
    height: int = field(init=False, default=0)
    mipmaps: int = field(init=False, default=0)
    gformatInt: int = field(init=False)
    gformat: GraphicFormat | None = field(init=False, default=None) 
    header_tale: tuple[int] = (0, 0, 1, 0, 0, 0, 0)
    end_tale: tuple[int] = (0, 1)
    header_tale_pack: str = '<7I'
    end_tale_pack: str = '<BI'

    def __post_init__(self, raw):
        fBuffer = BytesIO(raw)
        fBuffer.read(calcsize(self.header_tale_pack))

        self.dsize = unpack('<I', fBuffer.read(4))[0]
        self.zdata = zlib.compress(fBuffer.read(self.dsize), 9)

        self.width, self.height, _gformat, self.mipmaps = unpack('<2HII', fBuffer.read(12))
        self.gformat, self.gformatInt = GraphicFormat.get_type(_gformat)
        self.end_tale = unpack(self.end_tale_pack, fBuffer.read(calcsize(self.end_tale_pack)))
        
        fBuffer.close()
    
    def is_valid_format(self):
        return self.gformat is GraphicFormat.RGBA
    
    def export(self, skip_info: bool = False, skip_image: bool = False):
        from dev.FileSystem.fs import FILESPATH
        fName = f"{self.id}_{self.index}"
        fSavePath = path.join(FILESPATH, "extract", "PIC", fName)

        if skip_image and skip_info:
            log.info(f"{fName}: Export cancelled. [False] value for exporting INFO and IMAGE.")
            return
        
        if not self.is_valid_format():
            log.info(f"{fName}: Export cancelled. Invalid type format.")
            return
        
        if not skip_info:           
            with open(f"{fSavePath}.json", mode="w") as fInfo:
                dmp = asdict(self)
                dmp.update({
                    'type': self.type.name,
                    'gformat': self.gformat.name,
                    'zdata': None,
                    'sig': int.from_bytes(self.sig, byteorder="little"),
                })
                dump(dmp, fInfo, indent=2, ensure_ascii=False)
                log.info(f"Export info-file {fName}.")

        if not skip_image:
            # export image
            iBuffer = zlib.decompress(self.zdata)
            Image.frombytes(
                self.gformat.name,
                (self.width, self.height),
                iBuffer, 'raw').save(f'{fSavePath}.dds', format='dds')
            log.info(f"Export data-file {fName}.")
    
    def import_modified(self):
        with Image.open(self.mod_path) as mod_file:
            mod_file.load()        
        new_data = mod_file.tobytes()
        self.dsize = len(new_data)
        self.zdata = zlib.compress(new_data, 9)     
        new_size = len(self.get_data())
        self.size = new_size
        self.width = mod_file.width
        self.height = mod_file.height

    def get_data(self):
        chunk_header = self.get_chunk_header()
        img_header = pack(self.header_tale_pack, *self.header_tale) + pack('<I', self.dsize)
        img_data = zlib.decompress(self.zdata)
        img_info = pack('<2H2I', *(self.width, self.height, self.gformatInt, self.mipmaps))
        img_end = pack(self.end_tale_pack, *self.end_tale)

        r_data = chunk_header + img_header + img_data + img_info + img_end
        return r_data



