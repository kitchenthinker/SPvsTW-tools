from dataclasses import dataclass
from dev.FileSystem.chunks.chunk import GameDataFileChunk
import zlib


@dataclass
class Chunk_Uknown(GameDataFileChunk):

    def __post_init__(self, raw):
        self.zdata = zlib.compress(raw, 9)

    def export(self):
        pass

    def import_modified(self):
        pass

    def get_data(self):
        r_data = self.get_chunk_header()
        r_data += zlib.decompress(self.zdata)
        return r_data
