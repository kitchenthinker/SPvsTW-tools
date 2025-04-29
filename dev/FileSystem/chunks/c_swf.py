from dataclasses import dataclass, field, asdict
from struct import pack, calcsize, unpack
from io import BytesIO
from os import path
from json import dump
from dev.Logs.logger import log
from dev.FileSystem.chunks.chunk import GameDataFileChunk


import zlib


@dataclass
class Chunk_SWF(GameDataFileChunk):

    @dataclass
    class SWF_add_info:
        id1: int
        id2: int

    dsize: int = field(init=False)
    header_tale: tuple[int] = (0, 0, 1)
    header_tale_pack: str = '<3I'
    fonts: list[SWF_add_info] = field(default_factory=list)
    images: list[SWF_add_info] = field(default_factory=list)
    swf_header_s: str = 'UEF'
    swf_header_c: str = 'FWS'
    swf_version_s: int = 8
    swf_version_c: int = 15

    def __post_init__(self, raw):

        # skip header tale
        fBuffer = BytesIO(raw)
        fBuffer.read(calcsize(self.header_tale_pack))

        counter_fonts = unpack('<I', fBuffer.read(4))[0]
        for i in range(counter_fonts):
            fnt = unpack('<2I', fBuffer.read(8))
            self.fonts.append(Chunk_SWF.SWF_add_info(*fnt))

        counter_images = unpack('<I', fBuffer.read(4))[0]
        for i in range(counter_images):
            img = unpack('<2I', fBuffer.read(8))
            self.images.append(Chunk_SWF.SWF_add_info(*img))

        self.dsize = unpack('<I', fBuffer.read(4))[0]
        # skip swf header
        fBuffer.read(4)
        self.zdata = zlib.compress(fBuffer.read(self.dsize - 4), 9)

    def export(self):
        from dev.FileSystem.fs import FILESPATH
        fName = f"{self.id}_{self.index}"
        fSavePath = path.join(FILESPATH, "extract", "SWF", fName)

        with open(f"{fSavePath}.swf_info", encoding="utf16", mode="w") as swfInfo:
            dmp = asdict(self)
            dmp.update({
                'type': self.type.name,
                'zdata': None,
                # 'font_name': self.font_name.decode("utf-8"),
                'sig': int.from_bytes(self.sig, byteorder="little"),
            })
            dump(dmp, swfInfo, indent=2, ensure_ascii=False)
            log.info(f"Export font-file {fName}.")

        with open(f"{fSavePath}.swf", mode="wb") as SWF:
            SWF.write(self.swf_header_c.encode('utf8'))
            SWF.write(pack('<B', self.swf_version_c))
            SWF.write(zlib.decompress(self.zdata))
            log.info(f"Export swf-file {fName}.")

    def import_modified(self):
        with open(self.mod_path, mode='rb') as mod_file:
            # skip 4 bytes header
            mod_file.read(4)

            current_pos = mod_file.tell()
            self.dsize = unpack('<I', mod_file.read(4))[0]
            mod_file.seek(current_pos)
            self.zdata = zlib.compress(mod_file.read(self.dsize), 9)

        new_size = len(self.get_data())
        self.size = new_size

    def get_data(self):
        r_data = self.get_chunk_header()
        r_data += pack(self.header_tale_pack, *self.header_tale)
        r_data += pack('<I', len(self.fonts))
        for fnt in self.fonts:
            r_data += pack('<2I', fnt.id1, fnt.id2)
        r_data += pack('<I', len(self.images))
        for img in self.images:
            r_data += pack('<2I', img.id1, img.id2)
        r_data += pack('<I', self.dsize)
        r_data += pack('<3sB', self.swf_header_s.encode('utf8'), self.swf_version_s)
        r_data += zlib.decompress(self.zdata)

        return r_data
