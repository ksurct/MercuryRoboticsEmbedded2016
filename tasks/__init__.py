from invoke import ctask as task, Collection, Context, Config
from invoke.runners import Runner
from paramiko.client import SSHClient, AutoAddPolicy

from .runners import RemoteRunner

EXCLUDED_FILES = [
    '.*',
]


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
def build(ctx, for_arm=False, with_basestation=False):
    excluded_file_list = ' '.join(("--exclude='{}'".format(f) for f in EXCLUDED_FILES))
    ctx.run('rsync -azvr --delete --delete-excluded {} --filter=":- .gitignore" ./ ./_build'.format(excluded_file_list))

    build_cmd = 'nix-build ./_build --show-trace'
    if for_arm:
        build_cmd += ' --option system armv7l-linux'
    if with_basestation:
        build_cmd += ' --arg mkBasestation true'
    ctx.run(build_cmd)


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
