import vimside
import vimside.logger

import os
import tempfile

LOGGER = vimside.logger.getLogger(__name__)

class SbtError(Exception):
    pass

def _create_classpath(filename, scala_version, ensime_version):
    template_filename = os.path.join(
        vimside.root(), 'resources', 'templates', 'build.sbt.template')
    temp_dir = tempfile.mkdtemp(suffix="_vimside")

    template = ''
    with open(template_filename, 'r') as fh:
        template = fh.read()


    build = (template.replace("_scala_version_", scala_version)
                     .replace("_server_version_", ensime_version)
                     .replace("_classpath_file_", filename))

    with open(os.path.join(temp_dir, "build.sbt"), "w") as fh:
        fh.write(build)

    code = os.system("cd %s && sbt saveClasspath" % temp_dir)

    if code:
        raise SbtError(code)


def classpath():
    ensime_version = vimside.config.get('ensime', 'ensime-version')
    scala_version = vimside.config.get('ensime', 'scala-version')
    classpath_dir = vimside.config.get('vimside', 'classpath-cache')

    cache_dir = os.path.join(vimside.config.get('vimside', 'cache-dir'), classpath_dir)

    filename = os.path.join(cache_dir, "CLASSPATH_%s_%s" % (scala_version, ensime_version))

    if not os.path.exists(filename):
        _create_classpath(filename, scala_version, ensime_version)

    with open(filename, "r") as fh:
        return fh.read()

def start_command(config):
    cp = classpath()
    cmd = ["java",
           "-cp", cp,
           "-Densime.config=%s" % config,
           "org.ensime.server.Server"]
    return cmd
