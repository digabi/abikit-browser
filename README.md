# abikit-browser

WebKit browser for local HTML pages (koe-ohje, digi-MAOL etc)

This is typically called from a shell script bundled with the actual content (such as [koe-ohje](https://github.com/digabi/koe-ohje)).

## Usage

Abikit Browser supports several useful command-line parameters which can learned from the source.

Abikit Browser can be killed by sending SIGKILL to PID specified by `-l`. You have to manually
remove the lock file.

To kill all your `abikit-browser` processes use `-n`:

```
abikit-browser -n bubba file:///somecontent.html &
abikit-browser -n bubba file:///somecontent.html &
abikit-browser -n bubba file:///somecontent.html &
pkill bubba
```

## Development and Webkit

When developing software for abikit browser (such as [koe-ohje](https://github.com/digabi/koe-ohje)) it's good to ensure that your system is using the same version of python pyqt5 version as Digabios. You can use https://caniuse.com/ to determine if the browser feature you want to use is available in Digabios.

Digabios is currently (18.6.2020) based on Debian Stretch. Stretch is using `pyqt5 5.7` which uses `Webkit 538` and that matches the version used in `Safari 7`. https://packages.debian.org/stretch/python-pyqt5

Next planned debian for Digabios is Buster. Buster is using `pyqt5 5.11` which uses `Webkit 602` and that matches the version used in `Safari 10` https://packages.debian.org/buster/python-pyqt5

If you have apt, you can check your systems pyqt5 version with command `apt list python-pyqt5`

You can check the Webkit verison of your pyqt5 by running this with python:

```python
from PyQt5.QtWebKit import qWebKitVersion
print(qWebKitVersion())
```

## License

(C) Matriculation Examination Board 2019

Licensed under GPL v3 except the logo `abikit-browser.svg` (see below).

Abikit Browser logo:

- Artist: Good Stuff No Nonsense
- License: CC Attribution 4.0
- For more: http://www.iconarchive.com/show/free-space-icons-by-goodstuff-no-nonsense.html
