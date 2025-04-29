from dataclasses import dataclass, field, asdict, InitVar
from struct import pack, calcsize, unpack
from io import BytesIO
from os import path
from json import dump, load

from dev.Logs.logger import log
from dev.FileSystem.chunks.chunk import GameDataFileChunk



@dataclass
class Chunk_Font(GameDataFileChunk):
    
    @dataclass
    class CharInfo:

        id: int
        ascii: str = ''
        page: int = 0
        uv_left: float = 0
        uv_top: float = 0
        uv_right: float = 0
        uv_bottom: float = 0
        offset_x: int = 0
        offset_y: int = 0
        scale_x: int = 0
        scale_y: int = 0
        xAdvance: tuple[int] = (0, 0)
        kernels: tuple[int] = (0, 0, 0)
        
    header_tale: tuple[int] = (0, 0, 1)
    header_tale_pack: str = '<3I'
    dsize: int = field(init=False)
    # 3 bytes
    UKNOWN_1: tuple[int] = field(init=False)
    pagesCount: int = field(init=False)
    charsCount: int = field(init=False)
    # 34 bytes
    UKNOWN_2: tuple[int] = field(init=False)
    offset_bitmapname: int = field(init=False)
    # 4 bytes
    UKNOWN_3: tuple[int] = field(init=False)
    # 1 byte
    size_fontname: int = field(init=False)
    # font name (size - 1 empty byte)
    font_name: str = ''
    table_null_size: int = field(init=False)
    # true <H else <I
    table_null_f16b: bool = field(init=False)
    chars: dict[int:CharInfo] = field(init=False, default_factory=dict)
    # 6 bytes
    UKNOWN_4: tuple[int] = field(init=False)    
    kernsCount: int = field(init=False)
    bitmap_title: str = ''
    
    @staticmethod
    def getPointFromUVmapping(UVLeft: float, UVTop: float, UVRight: float, UVBottom: float, WidthImg: int, HeightImg: int):
        x = UVLeft * WidthImg
        y = UVTop * HeightImg
        width = (UVRight * WidthImg) - x
        height = (UVBottom * HeightImg) - y
        return (x, y, width, height)

    @staticmethod
    def getUVmappingFromPoint(x, y, width, height: float, WidthImg, HeightImg: int):

        UVLeft = x / WidthImg
        UVTop = y / HeightImg
        UVRight = (x + width) / WidthImg
        UVBottom = (y + height) / HeightImg
        return (UVLeft, UVTop, UVRight, UVBottom)
    
    def __post_init__(self, raw):
        # skip header tale
        fBuffer = BytesIO(raw)
        fBuffer.read(calcsize(self.header_tale_pack))

        self.dsize = unpack('<I', fBuffer.read(4))[0]
        self.UKNOWN_1 = unpack('<3b', fBuffer.read(3))
        self.pagesCount, self.charsCount = unpack('<BH', fBuffer.read(3))
        self.UKNOWN_2 = unpack('34b', fBuffer.read(34))
        self.offset_bitmapname = unpack('<I', fBuffer.read(4))[0]
        self.UKNOWN_3 = unpack('4b', fBuffer.read(4))
        self.size_fontname = unpack('<B', fBuffer.read(1))[0] - 1
        self.font_name = unpack(f'{self.size_fontname}s', fBuffer.read(self.size_fontname))[0]

        # skip nulled byte from font_name
        fBuffer.read(1)
        # skip repeat of charsCount
        fBuffer.read(2)

        cur_pos = fBuffer.tell()
        counter_nulled_bytes = -1

        nulled_byte = 0
        while nulled_byte == 0:
            counter_nulled_bytes += 1
            nulled_byte = int.from_bytes(fBuffer.read(1))
            
        fBuffer.seek(cur_pos)
        if counter_nulled_bytes / 2 == self.charsCount:
            self.table_null_f16b = True
            self.table_null_size = self.charsCount * 2 + 2
        else:
            self.table_null_f16b = False
            self.table_null_size = self.charsCount * 4 + 4
        fBuffer.read(self.table_null_size)

        for i in range(self.charsCount):
            chr_bytes = fBuffer.read(2)
            charID = unpack('<H', chr_bytes)[0]
            chr_unicode = chr_bytes.decode('utf16')
            self.chars[charID] = Chunk_Font.CharInfo(charID, chr_unicode)
        
        self.UKNOWN_4 = unpack('6b', fBuffer.read(6))

        for chrID, item in self.chars.items():
            item.xAdvance = unpack('<BB', fBuffer.read(2))

        # skip table-8
        fBuffer.read(self.charsCount * 2)

        self.kernsCount = unpack('<H', fBuffer.read(2))[0]
        self.bitmap_title = unpack('1s', fBuffer.read(1))[0].decode("utf8")
        fBuffer.read(1)
        for chrID, item in self.chars.items():
            item.page = unpack('<HB', fBuffer.read(3))[1]
            item.uv_left, item.uv_top = unpack('<2f', fBuffer.read(8))
            item.uv_right, item.uv_bottom = unpack('<2f', fBuffer.read(8))
            item.offset_x, item.offset_y = unpack('<2h', fBuffer.read(4))
            item.scale_x, item.scale_y = unpack('<2H', fBuffer.read(4))
    
    def import_modified(self):
        with open(self.mod_path, mode='r', encoding='utf16') as mod_file:
            raw = load(mod_file)

        raw['chars'] = {int(k): v for (k, v) in raw['chars'].items()}
        sorted_chars = dict(sorted(raw['chars'].items()))

        self.charsCount = len(sorted_chars)

        if self.table_null_f16b:
            self.table_null_size = self.charsCount * 2 + 2
        else:
            self.table_null_size = self.charsCount * 4 + 4

        self.chars.clear()
        for key, f_char in sorted_chars.items():
            f_char['id'] = key
            self.chars[key] = Chunk_Font.CharInfo(**f_char)

        self.size = len(self.get_data())
        self.dsize = self.size - 32
        self.offset_bitmapname = self.size - (27 * self.charsCount) - 2 - 76

    def export(self):
        from dev.FileSystem.fs import FILESPATH
        fName = f"{self.id}_{self.index}"
        fSavePath = path.join(FILESPATH, "extract", "FONT", fName)
         
        with open(f"{fSavePath}.font", encoding="utf16", mode="w") as fInfo:
            dmp = asdict(self)
            dmp.update({
                'type': self.type.name,
                'zdata': None,
                'font_name': self.font_name.decode("utf-8"),
                'sig': int.from_bytes(self.sig, byteorder="little"),
            })
            dump(dmp, fInfo, indent=2, ensure_ascii=False)
            log.info(f"Export font-file {fName}.")

    def get_data(self):
        r_data = self.get_chunk_header()
        
        r_data += pack(self.header_tale_pack, *self.header_tale)
        r_data += pack('<I', self.dsize)
        r_data += pack('<3b', *self.UKNOWN_1)
        r_data += pack('<BH', self.pagesCount, self.charsCount)
        r_data += pack('34b', *self.UKNOWN_2)
        r_data += pack('<I', self.offset_bitmapname)
        r_data += pack('4b', *self.UKNOWN_3)
        r_data += pack('<B', self.size_fontname + 1)
        fnt_name = self.font_name.encode('utf8') if isinstance(self.font_name, str) else self.font_name
        r_data += pack(f'{self.size_fontname}s', fnt_name)
        r_data += b'\x00'

        r_data += pack('<H', self.charsCount)
        r_data += b'\x00' * (self.table_null_size - (2 if self.table_null_f16b else 4))

        r_data += pack('<H' if self.table_null_f16b else '<I', self.table_null_size)

        table_chars = b''
        table_xadvance = b''
        table_desc = b''

        for chrID, itm in self.chars.items():
            table_chars += pack('<H', chrID)
            table_xadvance += pack('<2B', *itm.xAdvance)
            
            info = (
                itm.id,
                itm.page,
                itm.uv_left,
                itm.uv_top,
                itm.uv_right,
                itm.uv_bottom,
                itm.offset_x,
                itm.offset_y,
                itm.scale_x,
                itm.scale_y
            )
            table_desc += pack('<HB4f2h2H', *info)

        r_data += table_chars
        r_data += pack('6b', *self.UKNOWN_4)
        r_data += table_xadvance
        r_data += b'\x08\x00' * self.charsCount
        r_data += pack('<H', self.kernsCount)
        r_data += pack('<sb', self.bitmap_title.encode(), 0)
        r_data += table_desc

        return r_data


@dataclass
class Chunk_Font_JSON(Chunk_Font):

    raw: InitVar[dict]

    def __post_init__(self, raw):
        print(1)
        raw['chars'] = {int(k): v for (k, v) in raw['chars'].items()}
        sorted_chars = dict(sorted(raw['chars'].items()))

        self.dsize = 0
        self.UKNOWN_1 = raw['UKNOWN_1']
        self.pagesCount = raw['pagesCount']
        self.charsCount = len(sorted_chars)
        self.UKNOWN_2 = raw['UKNOWN_2']
        self.offset_bitmapname = 0
        self.UKNOWN_3 = raw['UKNOWN_3']
        self.size_fontname = raw['size_fontname']
        self.font_name = raw['font_name']
        self.UKNOWN_4 = raw['UKNOWN_4']
        self.kernsCount = raw['kernsCount']
        self.bitmap_title = raw['bitmap_title']

        self.table_null_f16b = raw['table_null_f16b']
        if self.table_null_f16b:
            self.table_null_size = self.charsCount * 2 + 2
        else:
            self.table_null_size = self.charsCount * 4 + 4

        for key, f_char in sorted_chars.items():
            f_char['id'] = key
            self.chars[key] = Chunk_Font.CharInfo(**f_char)

        r_data_len = len(self.get_data())
        self.dsize = r_data_len - 32
        self.size = r_data_len
        self.charsCount = len(self.chars)
        self.offset_bitmapname = r_data_len - (27 * self.charsCount) - 2 - (76 - (0 if self.index == 0 else 0))