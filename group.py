from collections import OrderedDict
from device import Device


class Group:
    def __init__(self, name, need_hide):
        self.name = name
        self.need_hide = need_hide
        self.devices = OrderedDict()

    def add_device(self, name: str, device: Device):
        self.devices[name] = device
