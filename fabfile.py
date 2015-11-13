from os import path
from fabric.api import run, env, put, sudo
from fabric.contrib.project import rsync_project, upload_project

env.hosts = ['raspberrypi.local']
# env.hosts = ['192.168.1.107']
env.user = 'pi'
env.password = 'raspberry'

BASEPATH = path.dirname(__file__)


def test():
    rsync_project('/home/pi/code', './src', exclude=['*.pyc'])
    # upload_project('./src', '/home/pi/code')
    sudo('python ./code/src/server.py')
