from invoke.runners import Local


def rsync(remote_ctx, local, remote):
    runner = Local(remote_ctx)
    hostname = remote_ctx.config.remote_runner.hostname
    username = remote_ctx.config.remote_runner.username
    runner.run('rsync -pthrvz {local} {username}@{hostname}:{remote}'.format(**locals()))


def test(ctx, cmd):
    return ctx.run()
