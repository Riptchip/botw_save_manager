import pdb
import os
import sys
import datetime as dt
from distutils.dir_util import copy_tree

SWITCH = 'switch'
WIIU = 'wiiU'

HEADERS = {
    0x24e2, 0x24EE, 0x2588, 0x29c0,
    0x3ef8, 0x471a, 0x471b, 0x471e
}

VERSIONS = {
    "v1.0", "v1.1", "v1.2", "v1.3",
    "v1.3.3", "v1.4", "v1.5", "v1.6"
}

ITEMS = {
    "Item", "Weap", "Armo", "Fire", "Norm", "IceA", "Elec", "Bomb", "Anci", "Anim",
    "Obj_", "Game", "Dm_N", "Dm_A", "Dm_E", "Dm_P", "FldO", "Gano", "Gian", "Grea",
    "KeyS", "Kokk", "Liza", "Mann", "Mori", "Npc_", "OctO", "Octa", "Octa", "arro",
    "Pict", "PutR", "Rema", "Site", "TBox", "TwnO", "Prie", "Dye0", "Dye1", "Map",
    "Play", "Oasi", "Cele", "Wolf", "Gata", "Ston", "Kaka", "Soji", "Hyru", "Powe",
    "Lana", "Hate", "Akka", "Yash", "Dung", "BeeH", "Boar", "Boko", "Brig", "DgnO"
}

HASHES = {
    0x7B74E117, 0x17E1747B, 0xD913B769, 0x69B713D9, 0xB666D246, 0x46D266B6, 0x021A6FF2,
    0xF26F1A02, 0xFF74960F, 0x0F9674FF, 0x8932285F, 0x5F283289, 0x3B0A289B, 0x9B280A3B,
    0x2F95768F, 0x8F76952F, 0x9C6CFD3F, 0x3FFD6C9C, 0xBBAC416B, 0x6B41ACBB, 0xCCAB71FD,
    0xFD71ABCC, 0xCBC6B5E4, 0xE4B5C6CB, 0x2CADB0E7, 0xE7B0AD2C, 0xA6EB3EF4, 0xF43EEBA6,
    0x21D4CFFA, 0xFACFD421, 0x22A510D1, 0xD110A522, 0x98D10D53, 0x530DD198, 0x55A22047,
    0x4720A255, 0xE5A63A33, 0x333AA6E5, 0xBEC65061, 0x6150C6BE, 0xBC118370, 0x708311BC,
    0x0E9D0E75, 0x750E9D0E
}

class SaveManager():
    def __init__(self, type, source) -> None:
        if not os.path.exists(source):
            raise ValueError('Source folder does not exists')
        
        self.type = type
        self.source = source
        self.readerPos = 0
        
    def convert(self, destination):
        if not os.path.exists(destination):
            raise ValueError('Destination folder does not exists')
        
        copy_tree(destination, destination + '_backup_' + dt.datetime.now().strftime('%d-%m-%Y_%H.%M'))
        copy_tree(self.source, destination)
        
        for file in get_files_with_extension(destination, '.sav'):
            data = bytearray(open(file, 'rb').read())
            converted = data.copy()
            print(file)
            # pdb.set_trace()
            
            normalCount = 0
            pos = 0
            while pos < (len(data)/4):
                    
                if 'trackblock' in file and pos == 0:
                    converted[2:4] = bytes(reversed(converted[4:6]))
                    pos = 2
                    
                self.readerPos = pos * 4
                buffer = converted[self.readerPos:self.readerPos+4]
                
                # pdb.set_trace()
                if int.from_bytes(bytes(buffer), sys.byteorder, signed=False) in HASHES:
                    converted[self.readerPos:self.readerPos+4] = bytes(reversed(buffer))
                    
                    pos += 1
                elif not item_in_buffer(buffer):
                    converted[self.readerPos:self.readerPos+4] = bytes(reversed(buffer))
                    normalCount += 1
                else:
                    pos += 1
                    for i in range(16):
                        self.readerPos = (pos + (i * 2)) * 4
                        buffer = converted[self.readerPos:self.readerPos+4]
                        converted[self.readerPos:self.readerPos+4] = bytes(reversed(buffer))
                    
                    pos += 30
                
                pos += 1
                
            open(file, 'wb').write(converted)            
            


def item_in_buffer(buffer):
    try:
        return any([item in buffer.decode('utf-8') for item in ITEMS])
    except UnicodeDecodeError:
        return False

def get_files_with_extension(folder, ext):
    filesFound = []
    
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(ext):
                filesFound.append(os.path.join(root, file))
    
    return filesFound

if __name__ == '__main__':
    # sm = SaveManager(SWITCH, 'D:\\Users\\Natha\\Emulators\\Wii U Updates\\usr\\save\\00050000\\101c9400\\user\\80000001')
    # sm = SaveManager(SWITCH, 'C:\\Users\\Natha\\Downloads\\yuzu saves')
    sm = SaveManager(SWITCH, 'test')
    # sm.convert('test')
    sm.convert('D:\\Users\\Natha\\Emulators\\Wii U Updates\\usr\\save\\00050000\\101c9400\\user\\80000001')
