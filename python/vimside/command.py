import logging
import sexp
import os
import tempfile
import subprocess
import time
import socket
import concurrent.futures
import vimside.rpc

from vimside.rpc.SwankConnection import SwankConnection



logger = logging.getLogger("vimside-server-command")
VIMSIDE_ROOT = os.path.join(os.path.dirname(__file__), "..", "..") 

class NoEnsimeConf(Exception):
    pass

class SbtError(Exception):
    pass

def _FindEnsimeConf(_dir):
    file_name = ".ensime"
    while _dir != "/":
        conf = os.path.join(_dir, file_name)
        logger.debug("Checking %s", conf)

        if os.path.exists(conf):
            return conf

        _dir = os.path.dirname(_dir)

    raise NoEnsimeConf

def _LoadEnsimeConf(env, filename):
    with open(filename, "r") as f:
        env.conf = sexp.load(f)

def _CreateClassPath(filename, scala_version, ensime_version):
    template_filename = os.path.join(VIMSIDE_ROOT, "templates/build.sbt.template")
    temp_dir = tempfile.mkdtemp(suffix="vimside_")

    template = ""
    with open(template_filename, "r") as f:
        template = f.read()

    build = (template.replace("_scala_version_", scala_version)
                     .replace("_server_version_", ensime_version)
                     .replace("_classpath_file_", filename))

    with open(os.path.join(temp_dir, "build.sbt"), "w") as f:
        f.write(build)

    code = os.system("cd %s && sbt saveClasspath" % temp_dir)

    if code:
        raise SbtError(code)


def _GetClassPath():
    cache_dir = os.path.join(VIMSIDE_ROOT, "data", "classpath")

    ensime_version = "0.9.10-SNAPSHOT"
    scala_version = "2.11.6"

    filename = os.path.join(cache_dir, "CLASSPATH_%s_%s" % (scala_version, ensime_version))

    if not os.path.exists(filename):
        _CreateClassPath(filename, scala_version, ensime_version)

    with open(filename, "r") as f:
        return f.read()

def _GetEnsimeCmd(conf_file):
    cp = _GetClassPath()
    cmd = ["java",
           "-cp", cp,
           "-Densime.config=%s" % conf_file,
           "org.ensime.server.Server"]

    return cmd

def _StartEnsime(env, conf_file):
    cmd = _GetEnsimeCmd(conf_file)
    with open("/tmp/ENSIME_LOG", "a") as f:
        env.ensime_process = subprocess.Popen(cmd, stdout = f, stderr = f)

def _SetupSocket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", port))

    return s

def _SetupConnection(env):
    port_file = os.path.join(env.conf["cache-dir"], "port")

    port = 0
    with open(port_file, "r") as f:
        port = int(f.read())

    socket = _SetupSocket(port)
    env.initialize_connection(SwankConnection(socket))

def _CreateCacheDir(env):
    if not os.path.exists(env.conf["cache-dir"]):
        os.mkdir(env.conf["cache-dir"])


def StartEnsime(env):
    if env.connection is not None:
        print("Vimside already running")
        return

    ensime_conf = _FindEnsimeConf(env.cwd)
    _LoadEnsimeConf(env, ensime_conf)
    _CreateCacheDir(env)

    _StartEnsime(env, ensime_conf)

    time.sleep(4)

    _SetupConnection(env)


def StopEnsime(env):
    try:
        env.connection.responseFuture(vimside.rpc.shutdown_server()).result(5)
    except concurrent.futures.TimeoutError:
        env.ensime_process.kill()


def ReloadFile(env, filename):
    if env.is_ready():
        env.connection.responseFuture(vimside.rpc.typecheck_file(filename))
    return 0
