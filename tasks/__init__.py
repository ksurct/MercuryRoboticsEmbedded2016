from invoke import ctask as task, Collection
from invoke.runners import Runner
from paramiko.client import SSHClient, AutoAddPolicy

from .runners import RemoteRunner


@task
def run(ctx):
    ctx.run('hostname')
    ctx.run('echo foo')


ns = Collection(run)
ns.configure(
    {
        'runner': RemoteRunner,
        'remote_runner': {
            'hostname': 'linux.cis.ksu.edu',
            'username': 'aaronschif'
        }
    }
)
