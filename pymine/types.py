class VarInt:
    def __init__(self, n):
        if not -0x80000000 < n < 0x7FFFFFFF:
            raise ValueError(
                "VarInt can only store numbers between -2147483648 and 2147483647"
            )
        self.n = n

    def pack(self):
        data = bytearray()
        n = self.n + 0x80000000
        while True:
            b = n & 0x7F
            if n:
                data.append(b | 0x80)
                n >>= 7
            else:
                data.append(b)
                return data
