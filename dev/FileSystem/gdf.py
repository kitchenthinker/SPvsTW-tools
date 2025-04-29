from dataclasses import dataclass, field, InitVar
from struct import pack, unpack
from io import BytesIO
from dev.Logs.logger import log
from dev.FileSystem.chunks.c_font import Chunk_Font
from dev.FileSystem.chunks.c_graphic import Chunk_Graphic
from dev.FileSystem.chunks.c_swf import Chunk_SWF
from dev.FileSystem.chunks.c_uknown import Chunk_Uknown
from dev.FileSystem.chunks.c_anim import Chunk_Animation
from dev.FileSystem.chunks.chunk import GameDataFileChunk, GameDataChunkType
import zlib


@dataclass
class GameDataFile:

    id: int
    raw_data: InitVar[bytes]
    archive: bool = False
    empty: bool = False
    analyzed: bool = False
    modified: bool = False
    chunks: list[GameDataFileChunk] = field(default_factory=list)

    def export_all_chunks(self):
        if self.empty:
            log.info(f"ID={self.id} is empty. Skip.")
        else:
            for chunk in self.chunks:
                self.export_chunk(chunk)

    def export_chunk(self, chunk: GameDataFileChunk):
        chunk.export()
        log.info(f"ID={self.id}\tChunk[{chunk.index}]={chunk.type.name} export.")

    def export_chunk_by_index(self, chunk_index: int):
        chunk = self.chunks[chunk_index]
        chunk.export()
        log.info(f"ID={self.id}\tChunk[{chunk_index}]={chunk.type.name} export.")

    def recreate_data(self) -> bytes:
        # if not self.modified:
        #     log.info(f"ID={self.id} is not modified. Skip.")
        #     return

        new_data = b''
        chunks_count = pack('<I', len(self.chunks))
        new_data += chunks_count

        for chunk in self.chunks:
            new_data += chunk.get_data()
        return zlib.compress(new_data, 9)
    
    def __post_init__(self, raw_data):
        self.analyze(raw_data=raw_data)

    def import_mod(self):
        for cnk in self.chunks:
            if cnk.modified:
                cnk.import_modified()

    def analyze(self, raw_data):

        def return_fileclass(chunk_size, chunk_sig, chunk_id, chunk_id2, chunk_index: int = 0):
            
            chunk_type = GameDataChunkType.get_type(chunk_sig)
            parents_init_data = {
                "id": chunk_id,
                "type": chunk_type,
                "sig": chunk_sig,
                "size": chunk_size,
                "second_id": chunk_id2,
                "raw": init_data.read(chunk_size - 16),
                "index": chunk_index,
            }
            if chunk_type is GameDataChunkType.GRAPHIC:
                return Chunk_Graphic(**parents_init_data)
            elif chunk_type is GameDataChunkType.FONT:
                return Chunk_Font(**parents_init_data)
            elif chunk_type is GameDataChunkType.SWF:
                return Chunk_SWF(**parents_init_data)
            elif chunk_type is GameDataChunkType.ANIM:
                return Chunk_Animation(**parents_init_data)
            else:
                return Chunk_Uknown(**parents_init_data)

        log.info(f"Analyze id={self.id}.")

        init_data = BytesIO(zlib.decompress(raw_data))

        chunks_count = unpack('<I', init_data.read(4))[0]
        self.empty = chunks_count == 0
        self.archive = chunks_count > 1

        if self.empty:
            log.info("Nothing to analyze, data is empty.")
            return

        for i in range(chunks_count):
            fchunk = return_fileclass(*unpack("<I4sII", init_data.read(16)), i)
            # TODO: Deleta after checking anim
            ###
            if fchunk.type is GameDataChunkType.ANIM:
                fchunk.export()
            ###
            self.chunks.append(fchunk)
            log.info(f"ID={self.id}\tChunk[{i}]={fchunk.type.name} analyzed and added to GameDataFile.")            

        init_data.close()
        self.analyzed = True
