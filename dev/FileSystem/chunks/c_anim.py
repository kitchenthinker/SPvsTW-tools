from dataclasses import dataclass, field, asdict
from struct import pack, calcsize, unpack
from io import BytesIO
from os import path
from json import dump, load
from dev.Logs.logger import log
from dev.FileSystem.chunks.chunk import GameDataFileChunk


import zlib


@dataclass
class Chunk_Animation(GameDataFileChunk):

    @dataclass
    class AnimInfo:
        x: int = 0
        y: int = 0
        w: int = 0
        h: int = 0

    h_tail: tuple[int] = field(init=False)
    UKNOWN_1: tuple[int] = field(init=False)
    UKNOWN_2: tuple[int] = field(init=False)
    UKNOWN_3: tuple[int] = field(init=False)
    frames: int = field(init=False)
    info: dict[int:AnimInfo] = field(init=False, default_factory=dict)

    def __post_init__(self, raw):

        # skip header tale
        fBuffer = BytesIO(raw)
        if self.size < 50:
            self.h_tail = None
            self.UKNOWN_1 = None
            self.UKNOWN_2 = None
            self.frames = 0
            self.info = dict()
            self.UKNOWN_3 = zlib.compress(fBuffer.read())
        else:
            self.h_tail = unpack('<4I', fBuffer.read(16))
            luk1 = 26 if self.h_tail[-1] == 0 else 34
            self.UKNOWN_1 = unpack(f'<{luk1}b', fBuffer.read(luk1))
            self.frames = unpack('<I', fBuffer.read(4))[0]

            for i in range(self.frames):
                id, x, y, _ = unpack('<4I', fBuffer.read(16))
                self.info[id] = Chunk_Animation.AnimInfo(x=x, y=y)

            self.UKNOWN_2 = unpack('<18b', fBuffer.read(18))
            # skip second counter frames
            fBuffer.read(4)
            for i in range(self.frames):
                id, w, h, _ = unpack('<4I', fBuffer.read(16))
                self.info[id].w = w
                self.info[id].h = h

            self.UKNOWN_3 = zlib.compress(fBuffer.read())

    def export(self):
        from dev.FileSystem.fs import FILESPATH
        fName = f"{self.id}_{self.index}"
        fSavePath = path.join(FILESPATH, "extract", "ANIM", fName)

        with open(f"{fSavePath}.anim_info", encoding="utf16", mode="w") as animInfo:
            dmp = asdict(self)
            dmp.update({
                'type': self.type.name,
                'zdata': None,
                'UKNOWN_1': None,
                'UKNOWN_2': None,
                'UKNOWN_3': None,
                'sig': int.from_bytes(self.sig, byteorder="little"),
            })
            dump(dmp, animInfo, indent=2, ensure_ascii=False)
            log.info(f"Export anim-file {fName}.")

    def import_modified(self):
        with open(self.mod_path, mode='r', encoding='utf16') as mod_file:
            raw = load(mod_file)

        raw['info'] = {int(k): v for (k, v) in raw['info'].items()}

        for key, frame in raw['info'].items():
            self.info[key] = Chunk_Animation.AnimInfo(**frame)

    def get_data(self):
        r_data = self.get_chunk_header()
        if self.size < 50:
            r_data += zlib.decompress(self.UKNOWN_3)
        else:
            r_data += pack('<4I', *self.h_tail)
            r_data += pack(f'<{len(self.UKNOWN_1)}b', *self.UKNOWN_1)
            r_data += pack('<I', self.frames)

            for key, frm in self.info.items():
                r_data += pack('<4I', key, frm.x, frm.y, 0)

            r_data += pack('<18b', *self.UKNOWN_2)

            r_data += pack('<I', self.frames)

            for key, frm in self.info.items():
                r_data += pack('<4I', key, frm.w, frm.h, 0)
            r_data += zlib.decompress(self.UKNOWN_3)

        return r_data
