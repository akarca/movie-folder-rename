from fabric.api import run, env, roles, sudo, cd, execute, local, settings, put
from fabric.context_managers import prefix
from fabric.contrib.files import exists, append

env.use_ssh_config = True
env.forward_agent = True
env.roledefs = {
    'osmc': ['osmc']
}

@roles('osmc')
def deploy():
    with cd("/home/osmc/movie-folder-rename"):
        run("git pull origin master")
