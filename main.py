from controller import Controller
from device import Device


def main():
    controller = Controller('192.168.0.117', 1883, 'devices.txt')

    while True:
        command = input('command: ').strip()

        if command in ['q', 'quit', 'exit']:
            break

        controller.process_command(command)

    controller.disconnect()


if __name__ == '__main__':
    main()
