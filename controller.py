import paho.mqtt.client as mqtt
from device import Device


class Controller:
    def __init__(self, address, port = 1883):
        self.devices = dict()
        self.client = self.init_client()
        self.client.connect(address, port, 60)
        self.client.loop_start()

    def init_client(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.on_message = self.on_message

        return client

    def on_connect(self, client, userdata, flags, rc):
        print(f'Connected with result code {rc}')

    def on_disconnect(self, client, userdata, rc):
        print(f'Disconnected with code. {rc}')

    def on_message(self, client, userdata, msg):
        for device in self.devices.values():
            if device.update_from_topic(msg.topic, msg.payload):
                return

        print(msg.topic + " " + str(msg.payload))

    def add_device(self, name: str, device: Device):
        self.devices[name] = device
        self.client.subscribe(device.state_topic)
        self.client.subscribe(device.value_topic)

    def process_command(self, command):
        if not command:
            return

        args = command.split()

        if len(args) == 0 or len(args) > 3:
            print('Invalid command')
            return

        device = self.devices.get(args[0], None)

        if device is None:
            print(f'Unknown device')
            return

        if len(args) == 1:
            device.log()
            return

        device.set_state(self.client, args[1])

        if len(args) == 3:
            device.set_value(self.client, args[2])

    def disconnect(self):
        self.client.disconnect()