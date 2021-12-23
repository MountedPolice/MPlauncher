import shutil

from PyQt5 import QtCore, QtGui, QtWidgets
import install_ui
import os
import threading
import patoolib
from requests import get
from sys import exit

import cfg


def get_app_path(app):
    path = os.getcwd() + "\\apps\\"+ app +"\\" + cfg.app_files.get(app)
    return path

def is_app_installed(app):
    return os.path.exists(get_app_path(app))

def launch(app, username):
    if app == "D":
        command = _java_comma(username)
    else:
        command = _all_comma(app, username)
    os.system(command)
    exit()

def install(app, signal):
    app_filename = os.getcwd() + '\\apps\\' + app
    file_name = os.getcwd() + '\\temp\\' + app + '.rar'
    url = 'https://github.com/MountedPolice/MPlauncher/releases/download/asd/' + app + '.rar'
    with open(file_name, "wb") as file:
        response = get(url)
        file.write(response.content)
    outpath = os.getcwd() + "\\apps\\" + app
    try:
        shutil.rmtree(app_filename)
    except:
        pass

    os.mkdir(outpath)
    patoolib.extract_archive(file_name, outdir=outpath)
    os.remove(file_name)
    file.close()
    signal.emit("")
    exit()

def _java_comma(username):
    path = os.getcwd() + '\\apps\\D\\javafx-sdk-11.0.2\\lib'
    comma = """java --module-path "jfxpath" --add-modules javafx.controls,javafx.fxml,javafx.graphics,javafx.web -jar """\
            +get_app_path("D")+""" username 78.24.217.186 2414 2417 businessapp zjekgf7tvj6go57ky3zv4w645wf1mipya9"""
    comma = comma.replace("jfxpath", path)
    comma = comma.replace("username", username)
    return comma

def _all_comma(app, username):
    comma = get_app_path(app) + ' ' + cfg.launch_args.get(app)
    comma = comma.replace("username", username)
    return comma