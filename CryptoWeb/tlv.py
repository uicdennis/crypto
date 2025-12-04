import binascii
from typing import Union

group0 = '''
dfee2d0100\
9c0100\
5f2a020840\
5f360102\
9f0206000000000001\
dfef5906000000000444\
dfef6f0130\
dfef6e020d0d\
9f0306000000000000\
9f09020002\
9f15020000\
9f1a020840\
9f40056000003000\
9f660430004000\
9f6d020001\
9f7c140000000000000000000000000000000000000000\
dfee28030008e8\
dfee29030068e8\
dfee3406000000010000\
dfee3503000601\
dfee3606000000008000\
dfee370103\
dfee380100\
df812205f850acf800\
df812005f850aca000\
df8121050000000000\
dfec1b04ffffffff\
dfed4a020006\
dfed5a080000800000000000\
dfee5c0401500000\
dfee700100\
dfee71020000\
dfee72020000\
dfee73020000\
dfee740100\
dfee1d0504042a0c31\
dfee7d0101\
9f4e1e000000000000000000000000000000000000000000000000000000000000\
9f530100\
dfee6b080000000000000000\
dfee4402ddff\
dfee7e0100\
dfee1c0103\
dfef29020000\
dfed180101\
9a03241216\
9f2103054936
'''

test = '''
9c0100\
5f2a020840\
5f360102\
9f0206000000000001\
9f0306000000000000
'''

test2 = '''
dfee2d0100\
dfef5906000000000444\
dfef6f0130\
dfef6e020d0d\
'''

txn_data_record = '''
df8116161b000000000000000000000000000000000000000000\
df81290830f0f000b0f0ff00dfec1c1e08030003ff001b00000000ff00000000000000000000000000000000ff00\
dfee120affffff0200223d20000fdfee2602e100dfee4c0103dfef4c06000000000000dfef4d00ff8105820180\
4f07a0000000041010500a4d61737465724361726457a1125413cccccccc1513d2012ccccccccccccccc\
57c118855a31e91d0641d4c0c681a30fd97a86fc1af00891bc8352\
5aa1085413cccccccc15135ac110cca41680b767ba798e9aa28a3d825fa4\
5f24032012315f25030601015f280200565f340100820259808407a0000000041010\
8e0a00000000000000001f038f01f3950504400000019a032412239b0200009c01009f0100\
9f02060000000001009f03060000000000009f0607a00000000410109f0702ff009f09020002\
9f0d05f8406420009f0e0500108800009f0f05f86064f8009f10120110a000002c0800000000000000037501ff\
9f150211119f16009f1a0208409f1c009f1d086cff0000000000009f1e0839543139303432389f2103063723\
9f2608e120c07356ea3dd89f2701809f2a01029f33030008089f34031f03029f3501229f360236c3\
9f3704cf5f09a29f3901079f400500000000009f4104000000159f4e009f5301009f6d020001\
dfee76050440000001ff81061edf8115060000000000ff9f42020978df810b0100df810e0100df810f0100ffee0105dfee300100'''

ppse_rsp = '6F55840E325041592E5359532E4444463031A543BF0C4061204F07A0000001523010500E44696E65727320436C75622030318701019F2A0106611C4F07A0000003241010500E44696E65727320436C7562203032870102'
ppse_rsp_2 = '6F59840E325041592E5359532E4444463031A547BF0C4461204F07A0000001523010500E44696E65727320436C75622030318701019F2A0106611C4F07A0000003241010500E44696E65727320436C75622030328701029F350122'

TAG_INIT_STATE = 0
TAG_SINGLE_BYTE = 1
TAG_EXTRA_BYTE = 2
TAG_FINAL_BYTE = 3
LEN_INIT_STATE = 4
LEN_SINGLE_BYTE = 5
LEN_EXTRA_BYTE = 6
LEN_FINAL_BYTE = 7
VALUE_INIT_STATE = 8
VALUE_FINAL_STATE = 9

class TLV:
    def __init__(self, tag: bytes = b'', length: bytes = b'', value: Union[list, bytes] = b''):
        self._tag = tag
        self._len = length
        self._value = value

    @property
    def tag(self) -> bytes:
        return self._tag

    @tag.setter
    def tag(self, tag):
        self._tag = tag

    @property
    def len(self) -> bytes:
        return self._len

    @property
    def valuelen(self) -> int:
        return len(self._value)

    @len.setter
    def len(self, length: bytes):
        self._len = length

    @property
    def value(self) -> bytes:
        if isinstance(self._value, bytes):
            return self._value
        else:
            sz = ''
            for tlv in self._value:
                sz = sz + tlv.tlv()
            return binascii.unhexlify(sz)

    @value.setter
    def value(self, value: Union[list, bytes]):
        self._value = value
        if isinstance(self._value, bytes):
            value_length = len(value)
        elif isinstance(self._value, list):
            value_length = 0
            for tlv in self._value:
                value_length = value_length + tlv.valuelen
        if self._len == b'':
            if value_length < 128:
                self._len = value_length.to_bytes(1, 'big')
            elif value_length < 256:
                self._len = b'\x81' + value_length.to_bytes(1, 'big')
            else:
                self._len = b'\x82' + value_length.to_bytes(1, 'big')

    @property
    def valuelist(self) -> list:
        return self._value if isinstance(self._value, list) else None
        # if isinstance(self._value, list):
        #     return self._value
        # else:
        #     return None

    def isConstructed(self) -> bool:
        return (self._tag[0] & 0x20)

    def tlv(self, isUpper: bool = True) -> str:
        bs = self.tag + self.len + self.value
        return bs.hex().upper() if isUpper else bs.hex()
        # if isUpper:
        #     return bs.hex().upper()
        # else:
        #     return bs.hex()

    def dump(self, indent: int = 0) -> str:
        # print(' '*indent, 'Tag =', self._tag.hex().upper())
        # print(' '*indent, 'Len =', self._len.hex().upper())
        # if type(self._value) is bytes:
        #     print(' '*indent, 'Value =', self._value.hex().upper())

        sz = ' '*indent + self._tag.hex().upper() + ' ' + self._len.hex().upper()
        print(' '*indent, self._tag.hex().upper(), ' ', self._len.hex().upper(), end=' ')
        if type(self._value) is bytes:
            sz = sz + ' ' + self._value.hex().upper()
            print(self._value.hex().upper())
        else:
            print('')

        return sz
class TLVParser:
    def __init__(self, tlvstream: str = None, tlvbytes: bytes = None):
        self._tlv_list = []
        self._tag_list = []     # debug
        if tlvstream:
            # self.stream = binascii.unhexlify(tlvstream)
            self.stream = bytes.fromhex(tlvstream)
        elif tlvbytes:
            self.stream = tlvbytes
        else:
            raise ValueError("Either tlvstream or tlvbytes must be provided.")

    @property
    def tlvlist(self) -> list:
        return self._tlv_list

    def parse(self, stream: bytes = None):
        if not stream:
            bs = self.stream
        else:
            bs = stream
        state = TAG_INIT_STATE
        # tlv = TLV()
        len_byte = 1
        length = 0
        index = 0
        tag = b''
        v = b''
        max_index = len(bs)
        tlvlist = []
        while index < max_index:
        # for by in bs:
            by = bs[index]
            if state == TAG_INIT_STATE:
                tlv = TLV()
                tag = by.to_bytes(1, 'big')
                if (by & 0x1F) == 0x1F:
                    state = TAG_EXTRA_BYTE
                else:
                    state = LEN_INIT_STATE
                    tlv.tag = tag
            elif state == TAG_EXTRA_BYTE:
                tag = tag + by.to_bytes(1, 'big')
                if (by & 0x80) == 0:
                    state = LEN_INIT_STATE  #TAG_FINAL_BYTE
                    tlv.tag = tag
                    # print('tag = ', tag.hex().upper())
            elif state == LEN_INIT_STATE:
                tag = b''
                if by & 0x80:
                    len_byte = by & 0x7F
                    state = LEN_EXTRA_BYTE
                else:
                    length = by
                    state = VALUE_INIT_STATE    #LEN_FINAL_BYTE
            elif state == LEN_EXTRA_BYTE:
                assert len_byte != 0
                length = length * 256 + by
                len_byte = len_byte - 1
                if len_byte == 0:
                    state = VALUE_INIT_STATE    #LEN_FINAL_BYTE
            elif state == VALUE_INIT_STATE:
                tlv.value = bs[index:(index+length)]
                self._tlv_list.append(tlv)
                tlvlist.append(tlv)
                # print(type(tlv))
                # print('tag = ', tlv.tag.hex().upper())
                ret = 0
                if tlv.isConstructed():
                    # print('  ---> ', bs[index:(index+length)])
                    ret, retlist = self.parse(bs[index:(index + length)])
                    # print('Ret = ', ret, ', index = ', index)
                    # print('Current Tag = ', tlv.tag.hex())
                    tlv.value = retlist
                    index = index + ret
                    state = TAG_INIT_STATE #VALUE_FINAL_STATE
                else:
                    state = TAG_INIT_STATE #VALUE_FINAL_STATE
                    # print('index = ', index)
                    # tlv.value = bs[index:(index+length)]
                    # tlv_list.append(tlv)
                    index = index + length
                    # tlv = TLV()
                    continue

            # print('  ==> tag = ', tlv.tag.hex().upper())
            if state != TAG_INIT_STATE:
                index = index + 1

        # return self._tlv_list
        # print("="*40)
        # tag_list = []
        # for node in tlvlist:
        #     tag_list.append(node.tag.hex())
        # print(tag_list)
        return index, tlvlist

    def findTag(self, tag: int) -> Union[bool, TLV]:
        if not self._tlv_list:
            return False

        # iterate Tag
        tag_hex = tag.to_bytes(4, 'big').hex()
        tag_hex = tag_hex.lstrip('0')
        for node in self._tlv_list:
            if node.tag.hex() == tag_hex:
                return node

        return False

    def dumpList(self) -> list:
        indent = 0
        # tag_num = 0
        result = []
        deep = []
        for tlv in self._tlv_list:
            result.append(tlv.dump(indent))
            if tlv.isConstructed():
                indent = indent + 2

                # tag_num = len(tlv.valuelist)
                deep.append(len(tlv.valuelist))
            else:
                if deep:
                    deep[-1] = deep[-1] - 1
                    while deep and not deep[-1]:
                        # 顯示所有子TLV
                        # 表示本身也顯示完畢
                        # 因此向上一層
                        deep.pop()
                        if deep:
                            deep[-1] = deep[-1] - 1
                        if indent:
                            indent = indent - 2

        return result

if __name__ == "__main__":
    # tag9C = TLV(b'\x9C', b'\x01', b'\x00')
    # print(tag9C.tlv())
    # tag9C.dump()

    # parse = TLVParser(test)
    # parse = TLVParser(group0)
    parse = TLVParser(ppse_rsp_2)
    parse.parse()

    parse.dumpList()
    # indent = 0

    # tag_list = []

    # tag_num = 0
    # for tlv in parse.tlvlist:
    #     tlv.dump(indent)
    #     if tlv.isConstructed():
    #         # tlv.dump(indent)
    #         indent = indent + 2

    #         tag_num = len(tlv.value)
    #         # for node in tlv.value:
    #         #     tag_list.append(node.tag.hex())
    #         # print(tag_list)
    #     else:
    #         if not tag_num and indent:
    #             indent = indent - 2
    #         if tag_num:
    #             tag_num = tag_num - 1

    tlv = parse.findTag(0x4F)
    print(tlv.value.hex())

