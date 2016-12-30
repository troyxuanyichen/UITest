
from collections import deque
 
class DataProcessor:
    def _next_raw(self):
        self.raw_x += 1
        x_ = self.raw_x % 200
        if self.raw_x // 200 % 2 == 0:
            return 2 - x_  / 50
        else:
            return x_ / 50 - 2

    def __init__(self):
        self.raw_x = 0
        self._rawdata = deque([self._next_raw() for _ in range(0, 500)]) 
        self._freq = [(800 if x % 2 else 20) for x in range(35) ]

    @property
    def message(self):
        return "Connected"

    @property
    def rawdata_array_whole(self):
        self._rawdata.popleft()
        self._rawdata.append(self._next_raw())
        return list(self._rawdata)

    @property
    def scalEngIndBuff(self):
        return [(y + 2) * 100 / 4 for y in list(self._rawdata)]   

    @property
    def rawfft_x(self):
        return [x for x in range(35)]

    @property
    def rawfft_y(self):
        return self._freq

    @property
    def histox(self):
        return [x for x in range(21)]

    @property
    def histoy(self):
        return (20000, 20000, 20000, 10000, 10000, 40000, 40000,40000,40000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

