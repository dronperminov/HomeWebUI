class Device:
    def __init__(self, dev, state, channel = None):
        self.dev = dev
        self.state = 0
        self.value = 100

        self.state_topic = f'/devices/{dev}/controls/{state}/on'
        self.value_topic = f'/devices/{dev}/controls/{channel}/on'

    def set_state(self, client, state):
        client.publish(self.state_topic, state)

    def set_value(self, client, value):
        client.publish(self.value_topic, value)

    def update_from_topic(self, topic, message):
        if topic == self.state_topic:
            self.state = int(message)
            return True

        if topic == self.value_topic:
            self.value = int(message)
            return True

        return False

    def log(self):
        print(f'{self.dev}: value = {self.value}, state = {self.state}')