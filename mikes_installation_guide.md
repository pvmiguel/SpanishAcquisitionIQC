Installation instructions on a clean RPM-Linux Machine

0. Get Git

## System Packages ##

### RPM-Based Distributions ###

Using your package manager (```yum``` on most RPM-based distros, ```dnf``` on Fedora), do the following

1. Run ```yum whatprovides */python-imaging```. If this package is not available, then you will need to install 
the EPEL repository onto your package manager repository list. Do this by running

```bash
	yum install epel-release
```

2. Using yum, install
	
    gcc-c++
	wx
	bzr
	mesa-libGLU-devel
	lapack-devel	
	python-pip
	python-imaging
	python-devel
	python-ivi
	wxPython
	kernel-devel
	xorg-x11-server-devel
	scipy
	swig


3. Run ```pip list | grep setuptools```. This should yield one line of output showing the version of the 
	[setuptools](https://pypi.python.org/pypi/setuptools) package installed on your machine. If no output
	is visible, install setuptools. Setuptools normally comes bundled with a Python installation, but some older
	versions of Python may not have it. To get it, run

	```bash
		wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
	```
	Find the file you just downloaded, and then run
	
	```
		sudo python ez_setup.py
	```

4. Upgrade pip using
	
	```bash
	sudo pip install --upgrade pip
	```

5. Upgrade nose using
	
	```bash
	sudo pip install --upgrade nose
	```
6. On Fedora, install redhat-rpm-config.
	
6. Install [traits](https://pypi.python.org/pypi/traits). This is a dependency for the ```enable``` library,
	which is itself a dependency for chaco, one of the graphics libraries. The installation from PyPI is
	currently broken, so you will need to use your package manager.
	

5. cd into the library directory and run

	sudo pip install enable-4.2.0.tar.gz
	sudo pip install chaco-4.2.0.tar.gz
	sudo pip install ObjectListView
	""	""	Pyparsing
			PubSub
            quantities
            nose-testconfig           
	
6. Get the ISO image from the site, and mount it using

	mount -o loop <iso-location>/NI-VISA-#.#.#.iso <mount-location>

7. cd into this directory and run the INSTALL shell script using

	./INSTALL
	
This needs to be run as root

8. Install Linux GPIB following the instructions in the other file

8. Run
	sudo pip install PyVISA==1.5



9. Upgrade numpy and scipy with pip
	
	sudo pip install --upgrade scipy

10. Install the NI-488 GPIB driver
