from invoke import ctask as task, Collection, Context, Config
from invoke.runners import Runner
from paramiko.client import SSHClient, AutoAddPolicy

from .runners import RemoteRunner


srv = Context(
    Config({
        'runner': RemoteRunner,
        'remote_runner': {
            'hostname': 'raspberrypi.local',
            'username': 'pi'
        },
}))


@task
def setup(ctx):
    if srv.run('test -d /nix', warn=True).ok:
        pass


@task
def build(ctx):
    ctx.run('nix-build --option system armv7l-linux')


@task
def install(ctx):
    result = ctx.run('realpath ./result')
    ctx.run('nix-copy-closure --to {}@{} {}'.format(
        srv.config.remote_runner.username,
        srv.config.remote_runner.hostname,
        result))
    srv.run('nix-env -i {}'.format(result))


ns = Collection(setup, build, install)
ns.configure({})
