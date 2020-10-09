"""
根据给定的类型完全随机的从它的值域中取值。
"""
import random


class Number(object):
    """

    """
    begin = 0
    end = 128

    def __getitem__(self, index):
        """
        """
        return random.randint(self.begin, self.end)

    def __len__(self):
        """
        """
        return self.end - self.begin


class Int(Number):
    begin = 0
    end = (1 << 32) - 1


class Float(Int):
    begin = 0
    end = (1 << 32) - 1

    def __getitem__(self, index):
        return random.randint(self.begin, self.end - 1) + random.random()
