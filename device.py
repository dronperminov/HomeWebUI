class Device:
    def __init__(self, dev, state, channel=None):
        self.dev = dev
        self.state = 0
        self.value = 100

        self.state_topic = '/devices/{dev}/controls/{state}/on'.format(dev=dev, state=state)
        self.value_topic = '/devices/{dev}/controls/{channel}/on'.format(dev=dev, channel=channel)
        self.state_topic_get = '/devices/{dev}/controls/{state}'.format(dev=dev, state=state)
        self.value_topic_get = '/devices/{dev}/controls/{channel}'.format(dev=dev, channel=channel)

    def set_state(self, client, state):
        client.publish(self.state_topic, state)

    def set_value(self, client, value):
        client.publish(self.value_topic, value)

    def update_from_topic(self, topic, message):
        if topic in [self.state_topic, self.state_topic_get]:
            self.state = int(message)
            return True

        if topic in [self.value_topic, self.value_topic_get]:
            self.value = int(message)
            return True

        return False

    def log(self):
        print('{dev}: value = {value}, state = {state}'.format(dev=self.dev, value=self.value, state=self.state))

    def to_json(self):
        return {"state": self.state, "value": self.value}