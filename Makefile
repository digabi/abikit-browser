default_build_number=1

deb:
	mkdir -p deb-root/usr/local/lib/abikit-browser
	cp abikit-browser.svg deb-root/usr/local/lib/abikit-browser/

	mkdir -p deb-root/usr/local/bin
	cp abikit-browser.py deb-root/usr/local/bin/abikit-browser

	chmod 755 deb-root/usr/local/bin/*

	if [ "x$(BUILD_NUMBER)" = "x" ]; then BUILD_NUMBER=$(default_build_number); echo "Using default build number $$BUILD_NUMBER"; fi; \
	fpm -C deb-root/ -s dir --name abikit-browser --architecture native -t deb --version "1.0.$$BUILD_NUMBER" --depends python --depends python-setproctitle --depends python-pyqt5.qtwebkit --depends gstreamer1.0-plugins-good --depends gstreamer1.0-plugins-ugly --depends gstreamer1.0-libav .
