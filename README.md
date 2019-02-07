# abikit-browser

WebKit browser for local HTML pages (koe-ohje, digi-MAOL etc)

This is typically called from a shell script bundled with the actual content (e.g. `koe-ohje`).

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

## License

(C) Matriculation Examination Board 2019

Licensed under GPL v3 except the logo `abikit-browser.svg` (see below).

Abikit Browser logo:
 * Artist: Good Stuff No Nonsense
 * License: CC Attribution 4.0
 * For more: http://www.iconarchive.com/show/free-space-icons-by-goodstuff-no-nonsense.html
