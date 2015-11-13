import locale
from invoke import ctask as task, Collection
from functools import partial
from invoke.runners import Local, Runner
from paramiko.client import SSHClient, AutoAddPolicy


class RemoteRunner(Runner):
    def __init__(self, *args, **kwargs):
        super(RemoteRunner, self).__init__(*args, **kwargs)
        self.context

    def start(self, command):
        self.ssh_client = SSHClient()
        self.ssh_client.load_system_host_keys()
        self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh_client.connect(self.context.remote_runner.hostname, username=self.context.remote_runner.username)
        self.ssh_channel = self.ssh_client.get_transport().open_session()
        if self.using_pty:
            self.ssh_channel.get_pty()
        self.ssh_channel.exec_command(command)

    def stdout_reader(self):
        return self.ssh_channel.recv

    def stderr_reader(self):
        return self.ssh_channel.recv_stderr

    def default_encoding(self):
        return locale.getpreferredencoding(True)

    def wait(self):
        return self.ssh_channel.recv_exit_status()

    def returncode(self):
        return self.ssh_channel.recv_exit_status()
