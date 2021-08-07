from controller import Controller
from device import Device


def main():
    controller = Controller("192.168.0.117")
    
    controller.add_device('Санузел', Device('wb-mdm3_14', 'K1', 'Channel 1'))
    controller.add_device('Балкон', Device('wb-mdm3_14', 'K2', 'Channel 2'))
    controller.add_device('Коридор', Device('wb-mdm3_14', 'K3', 'Channel 3'))
    controller.add_device('Бра_Андрей', Device('wb-mdm3_34', 'K1', 'Channel 1'))
    controller.add_device('Бра_Света', Device('wb-mdm3_34', 'K2', 'Channel 2'))
    controller.add_device('Спальня', Device('wb-mdm3_34', 'K3', 'Channel 3'))
    controller.add_device('Столешница', Device('wb-mdm3_30', 'K1', 'Channel 1'))
    controller.add_device('Гостиная', Device('wb-mdm3_30', 'K2', 'Channel 2'))
    controller.add_device('Кухня', Device('wb-mdm3_30', 'K3', 'Channel 3'))

    while True:
        command = input('command: ').strip()

        if command in ['q', 'quit', 'exit']:
            break

        controller.process_command(command)

    controller.disconnect()


if __name__ == '__main__':
    main()
