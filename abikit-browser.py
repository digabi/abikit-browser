#!/usr/bin/python2
# -*- coding: utf-8 -*-

import argparse, sys, subprocess, os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebKit import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import QWebView
from setproctitle import setproctitle
from os.path import expanduser

DEFAULT_APP_ICON_PATH='/usr/local/lib/abikit-browser/abikit-browser.svg'
DEFAULT_LOCAL_STORAGE_PATH="%s/.cache/digabi-koe" % expanduser("~")
DEFAULT_PROCNAME='abikit-browser'

procname = DEFAULT_PROCNAME

class SharedClass (QObject):
    @pyqtSlot(str)
    def copy_html_to_clipboard(self, value):
        xclip = subprocess.Popen("xclip -selection clipboard -target text/html -i".split(" "), stdin=subprocess.PIPE, shell=False)
        xclip.communicate(value.encode("utf-8"))
        xclip.wait()

    @pyqtSlot(str)
    def copy_text_to_clipboard(self, value):
        clipboard = QApplication.clipboard()
        clipboard.setText(value)

    @pyqtSlot(str)
    def write_to_stdout(self, value):
        print("[%s] %s" % (procname, value))
        sys.stdout.flush()

class Window (QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.view = QWebView(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.view)

        self.sharedclass = SharedClass(self)
        self.frame = self.view.page().mainFrame()
        self.frame.javaScriptWindowObjectCleared.connect(self.add_shared_object)

    def load_url (self, url):
        self.view.load(QUrl(url))

    def add_shared_object(self):
        self.frame.addToJavaScriptWindowObject("sharedclass", self.sharedclass)

sc = SharedClass()

def appExiting ():
    lockfileRemove()
    sc.write_to_stdout("window closed, exiting")

lockfile = ""

def lockfileWrite():
    if lockfile != "":
        LF = open(lockfile, "w")
        LF.write("%d" % os.getpid())
        LF.close()
        sc.write_to_stdout("Created lockfile %s" % lockfile)

def lockfileRemove():
    if lockfile != "":
        os.remove(lockfile)
        sc.write_to_stdout("Removed lockfile %s" % lockfile)

def main():
    global lockfile, procname

    parser = argparse.ArgumentParser()
    parser.add_argument('-W', '--width', dest='width', type=int, default=500, help='Browser window width')
    parser.add_argument('-H', '--height', dest='height', type=int, default=300, help='Browser window height')
    parser.add_argument('-x', '--positionx', dest='posx', type=int, default=1, help='Window position (X)')
    parser.add_argument('-y', '--positiony', dest='posy', type=int, default=1, help='Window position (Y)')
    parser.add_argument('-t', '--title', dest='title', type=str, default="Help", help='Window title')
    parser.add_argument('url', type=str, help='URL of the help file')
    parser.add_argument('-s', '--localstorage', dest='localstorage', type=bool, default=False, help='Write local storage to disk')
    parser.add_argument('-p', '--localstoragepath', dest='localstoragepath', type=str, default=DEFAULT_LOCAL_STORAGE_PATH, help='Path to local storage')
    parser.add_argument('-i', '--iconpath', dest='iconpath', type=str, default=DEFAULT_APP_ICON_PATH, help='Path to application icon')
    parser.add_argument('-l', '--lockfile', dest='lockfile', type=str, default='', help='Write lock file containing a PID to this file')
    parser.add_argument('-n', '--procname', dest='procname', type=str, default='', help='Set process name/title')
    parser.add_argument('-dev', '--devmode', dest='devmode', type=bool, default=False, help='Developer mode toggle')

    args = parser.parse_args()

    sc.write_to_stdout("starting")

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(appExiting)

    window = Window()

    window.resize(args.width, args.height)
    window.move(args.posx, args.posy)
    window.setWindowTitle(args.title)
    window.setWindowIcon(QIcon(args.iconpath))

    # Dev-environment debug variables
    if args.devmode:
        from PyQt5.QtWebKitWidgets import QWebInspector
        inspector = QWebInspector()
        window.view.page().settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        inspector.setPage(window.view.page())
        inspector.showMaximized()

    # Enable LocalStorage
    if args.localstorage:
        window.view.page().settings().setLocalStoragePath(args.localstoragepath)
        window.view.page().settings().setAttribute(QWebSettings.LocalStorageEnabled, True)
        sc.write_to_stdout("localstorage enabled, path: %s" % args.localstoragepath)

    if args.procname != "":
        procname = args.procname
        setproctitle(args.procname)
        sc.write_to_stdout("using process name %s" % args.procname)

    # Write lock file (if lock file path was set)
    lockfile = args.lockfile
    lockfileWrite()

    window.load_url(args.url)
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
