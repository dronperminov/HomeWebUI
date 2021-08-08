import re
import paho.mqtt.client as mqtt
from device import Device


class Controller:
    def __init__(self, address, port, devices_filename):
        self.devices = dict()
        self.client = self.init_client()
        self.client.connect(address, port, 60)
        self.client.loop_start()
        self.read_devices(devices_filename)

    def init_client(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.on_message = self.on_message

        return client

    def read_devices(self, filename):
        with open(filename, encoding='utf-8') as f:
            lines = [line for line in f.read().splitlines() if line]

        for line in lines:
            params = re.findall(r'\"[\w \-]+\"|[\w\-]+', line)
            params = [re.sub(r'"', '', param) for param in params]

            device = Device(params[1], params[2], params[3])
            self.add_device(params[0], device)

    def on_connect(self, client, userdata, flags, rc):
        print('Connected with result code {rc}'.format(rc=rc))

    def on_disconnect(self, client, userdata, rc):
        print('Disconnected with code. {rc}'.format(rc=rc))

    def on_message(self, client, userdata, msg):
        for device in self.devices.values():
            if device.update_from_topic(msg.topic, msg.payload):
                return

        print(msg.topic + " " + str(msg.payload))

    def add_device(self, name: str, device: Device):
        self.devices[name] = device
        self.client.subscribe(device.state_topic_get)
        self.client.subscribe(device.value_topic_get)

    def process_command(self, command):
        if not command:
            return

        args = re.findall(r'\"[\w \-]+\"|[\w\-]+', command)
        args = [re.sub(r'"', '', arg) for arg in args]

        if len(args) == 0 or len(args) > 3:
            print('Invalid command')
            return

        device = self.devices.get(args[0], None)

        if device is None:
            print('Unknown device')
            return

        if len(args) == 1:
            device.log()
            return

        device.set_state(self.client, args[1])

        if len(args) == 3:
            device.set_value(self.client, args[2])

    def disconnect(self):
        self.client.disconnect()