from pkgutil import get_data
from sys import executable, argv


def create_service():
    service_template = get_data(__package__, '/files/ksurobot.service').decode('UTF-8')

    service_cmd = "{} -m ksurobot robot".format(executable)

    service = service_template.format(**locals())

    return service


def install_service():
    text = create_service()
    with open('/etc/systemd/system/ksurobot.service', mode='w') as f:
        f.write(text)


def main():
    install_service()
