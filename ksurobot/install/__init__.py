from pkgutil import get_data
from sys import executable, argv


def create_service(service_cmd):
    service_template = get_data(__package__, '/files/ksurobot.service').decode('UTF-8')

    service = service_template.format(service_cmd=service_cmd)

    return service


def install_service():
    service_cmd = "{} -m ksurobot robot".format(executable)
    text = create_service(service_cmd)
    with open('/etc/systemd/system/ksurobot.service', mode='w') as f:
        f.write(text)


def install_service_video():
    text = create_service('/usr/bin/faucet 9001 --out /opt/vc/bin/raspivid -o - -t 0 -b 1000000')
    with open('/etc/systemd/system/ksurobot_video.service', mode='w') as f:
        f.write(text)


def main():
    install_service()
    install_service_video()
