from abc import abstractmethod, ABC
from dataclasses import dataclass, field, InitVar
from struct import pack
from enum import Enum


class GameDataChunkType(Enum):

    GRAPHIC = b'\xD9\x7E\x09\x24'
    FONT = b'\xCE\x81\x40\x04'
    UKNOWN = b''
    SWF = b'\x79\x19\x09\x10'
    ANIM = b'\x2E\xB2\x67\x0F'

    def get_type(value):
        try:
            _type = GameDataChunkType(value)
            return _type
        except ValueError:
            return GameDataChunkType.UKNOWN


@dataclass
class GameDataFileChunk(ABC):

    # Chunk header
    id: int
    type: GameDataChunkType
    sig: int
    size: int
    second_id: int
    ###

    index: int
    # bytes for analyze
    raw: InitVar[bytes]
    # store in zlib
    zdata: bytes = field(init=False, default=b'')
    modified: bool = False
    mod_path: str = ''

    @abstractmethod
    def export(self):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def import_modified(self):
        pass
    
    def get_chunk_header(self):
        return pack('<I4s2I', *(self.size, self.sig, self.id, self.second_id))