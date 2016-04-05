##Installation Instructions##

TODO: Make this prettier

Installation from 32-bit Scientific Linux 6.1 LiveCD:

1. Boot to LiveCD, log in with default user
2. Install to Hard Drive (double-click on desktop)

   1. Choose a keyboard (US English is fine)
   2. Basic Storage Devices
   3. Default hostname is fine
   4. America/Toronto w/ UTC
   5. Choose a root password; this can be changed later.
   6. Partition layout:

      * Don't touch sda1 or sda2 (that's Windows)
      * Default settings for "Replace Existing Linux System(s)" appear sane
      * Check the "review settings" checkbox and make sure things look OK

   7. Put a passwordless bootloader on /dev/sda

3. Reboot.
4. Post-install setup

   1. Create a regular user (eg. "jonathan"); no special settings are required
   2. Enable NTP ("Synchronize date and time over the network") and choose to speed up the initial sync

5. Configure sudo

   1. Run `su` and type in the root password
   2. Run `visudo` and find and uncomment the line "%wheel  ALL=(ALL)       NOPASSWD: ALL"

      * This step requires knowledge of vi! However the following should work:

            /NOPASSWD<enter>02x:x

        where <enter> is the enter key, and 0 is the zero key.

   3. Add the regular user to group "wheel": `usermod --append --groups wheel jonathan`

6. sudo yum update
7. Make changes to system settings, as desired. For example:

   * In the workspace switcher (bottom-right corner), 16 workspaces in 4 rows rather than 2 in 1 row
   * In System -> Preferences -> Keyboard Shortcuts, type Windows+Enter (displays as Mod4+Return) for starting a terminal
   * In System -> Preferences -> Power Management, set the display to never go to sleep
   * In System -> Preferences -> Screensaver, disable locking

8. Add EPEL repo (http://fedoraproject.org/wiki/EPEL)

   1. Visit http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-5.noarch.rpm in Firefox
   2. Agree to install
   3. Add the keys by running `sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6`

9. Install software packages

       sudo yum install bash-completion blas-devel dhcp freeglut-devel freetype-devel gcc gcc-c++ git gitk ipython kernel-devel lapack-devel libpng-devel make patch python-devel python-pip python-sphinx10 swig vim wxPython

   Note that python-sphinx10 requires the following: `sudo ln /usr/bin/sphinx-1.0-build /usr/bin/sphinx-build`

10. Reduce the available memory

       sudo vim /boot/grub/menu.lst
         Append "mem=4096M" to the "kernel" line
       sudo reboot

11. Install NI-VISA 5.0.0

   1. Get it from http://joule.ni.com/nidu/cds/view/p/id/2040/lang/en
      Also found on this machine at /home/jonathan/software/NI-VISA-5.0.0.iso, extracted to /home/jonathan/software/NI-VISA-5.0.0
   2. From the NI-VISA-5.0.0 directory, run `sudo bash INSTALL`
        Agree to everything except rebooting

12. Install Linux GPIB

   1. Get it from http://sourceforge.net/projects/linux-gpib/files/linux-gpib%20for%202.6.x%20kernels/
      Version 3.2.16 is found on this machine at /home/jonathan/software/linux-gpib-3.2.16.tar.gz, extracted to /home/jonathan/software/linux-gpib-3.2.16

   2. From the linux-gpib-3.2.16 directory, run `./configure --prefix=/usr`, `make`, and `sudo make install`
   3. There is a bug in Linux GPIB which has a fix submitted: http://sourceforge.net/tracker/?func=detail&aid=3394299&group_id=42378&atid=432942
      As of this writing, the fix has been accepted, but has not been made part of any downloadable version.
      If that changes (I expect as of version 3.2.17), these instructions should be altered to remove this step.

      The python_threads.patch file needs to be downloaded and applied by running `patch -p0 < python_threads.patch` from the linux-gpib-3.2.16 directory
      This has already been done to the version in /home/jonathan/software/linux-gpib-3.2.16

   4. From the linux-gpib-3.2.16/language/python directory, run `make`, and `sudo make install`
   5. Replace the sample interfaces and devices in /etc/gpib.conf with:

========8<=======BEGIN=======>8========
interface {
    minor = 0
    name = "usb"
    board_type = "ni_usb_b"
    pad = 0
    sad = 0
    timeout = T3s

    set-eot = yes
    master = yes
}
========8<========END========>8========

13. Configure NetworkManager to use one network card for the Internet and the other for the devices

    1. Open System -> Preferences -> Network Connections
    2. In the "Wired" tab, edit "Auto eth0"

       IPv4 Settings
         Method -> Manual
         Addresses -> Add -> 192.168.0.1 / 24 / 192.168.0.238
         Routes... -> Enable "Use this connection only for resources on its network"

       This is to make that network card work with the network switch and devices.

    3. In the "Wired" tab, edit "Auto eth1"

       Wired
         Cloned MAC Address -> BC:AE:C5:68:84:CC

       This is to make that network card work with the university network.
       That MAC address is the same as that of eth0. The university's DHCP server checks the MAC, so we fake it to be what it expects.

14. Configure dhcpd

    1. Add the following to /etc/dhcp/dhcpd.conf:

========8<=======BEGIN=======>8========
default-lease-time 600;
max-lease-time 7200;

# eth0
subnet 192.168.0.0 netmask 255.255.255.0 {
  range 192.168.0.100 192.168.0.199;
  option routers 192.168.0.238;
}

# The network switch.
host switch {
  hardware ethernet c4:3d:c7:a2:6d:41;
  # Default is .239
  fixed-address 192.168.0.238;
}

# This computer.
host computer {
  hardware ethernet bc:ae:c5:68:84:cc;
  fixed-address 192.168.0.1;
}

# The AWG5014B.
host awg {
  hardware ethernet 00:d0:c9:b5:ee:63;
  fixed-address 192.168.0.10;
}

# The DPO7104.
host oscilloscope {
  hardware ethernet 00:d0:c9:b4:e7:e0;
  fixed-address 192.168.0.11;
}

# The SMF100A.
host microwave {
  hardware ethernet 00:e0:33:5b:83:97;
  fixed-address 192.168.0.20;
}

# The Windows machine.
host windows {
  hardware ethernet 00:1a:a0:8b:9a:4c;
  fixed-address 192.168.0.42;
  # For forwarding to work:
  option routers 192.168.0.1;
  option domain-name-servers 4.2.2.1;
}
========8<========END========>8========

       Note that these settings are for the devices that are configured as of this writing.
       To update this configuration, see usage.txt -> Devices -> Ethernet
       Remember to update this file as well.
    2. System -> Administration -> Services -> dhcpd -> Enable

15. Configure udev

    1. Create the file /etc/udev/rules.d/99-gpib.rules, and insert the following 2 lines:

========8<=======BEGIN=======>8========
KERNEL=="gpib0", MODE="0666", RUN+="/usr/bin/logger More GPIB", RUN+="/usr/sbin/gpib_config --minor 0"
ACTION=="remove", ENV{ID_VENDOR_ID}=="3923", ENV{ID_MODEL_ID}=="709b", RUN+="/usr/bin/logger Less GPIB", RUN+="/sbin/rmmod ni_usb_gpib gpib_common"
========8<========END========>8========

    2. Create the file /etc/udev/rules.d/99-vsrc.rules, and insert the following 1 line:

========8<=======BEGIN=======>8========
SUBSYSTEMS=="usb", ATTRS{idVendor}=="3923", ATTRS{idProduct}=="7166", MODE="0666"
========8<========END========>8========

16. Reboot

17. Install Python packages

    1. Those which can be installed easily

        sudo pip-python install numpy ObjectListView
        sudo pip-python install pyparsing quantities
        sudo pip-python install chaco enable
        sudo pip-python install matplotlib
        sudo pip-python install ez_setup nose nose-testconfig
        sudo pip-python install scipy

        NB. Version 1.0.1 of matplotlib does not display the multipler for 3D plots.
            If this functionality is desired, the latest development version should be installed from:

                https://github.com/matplotlib/matplotlib

            If a newer version is released, these instructions should be altered to remove this note.

    2. And those which cannot

       * PyVISA

         1. Get it from http://sourceforge.net/projects/pyvisa/files/PyVISA/
            Version 1.3 is found on this machine at /home/jonathan/software/PyVISA-1.3.tar.gz, extracted to /home/jonathan/software/PyVISA-1.3
         2. From the PyVISA-1.3 directory, run `sudo python setup.py install`

       * PyPubSub

         1. Get it from http://sourceforge.net/projects/pubsub/files/pubsub/
            Version 3.1.1b1 is found on this machine at /home/jonathan/software/PyPubSub-3.1.1b1.zip, extracted to /home/jonathan/software/PyPubSub-3.1.1b1
         2. From the PyPubSub-3.1.1b1 directory, run `touch cheese.txt`, and `sudo python setup.py install`

    3. Also fix those which are buggy

       * ObjectListView

         There is a bug in ObjectListView which has a fix submitted: http://sourceforge.net/tracker/?func=detail&aid=3394298&group_id=225207&atid=1064159
         As of this writing, the fix has not yet been accepted, which means it's not part of any downloadable version.
         If that changes, these instructions should be altered to remove this step.

         The show_zero.patch file needs to be downloaded and applied by running `sudo patch -p1 < show_zero.patch` from /usr/lib/python2.6/site-packages/ObjectListView
         This has already been done to the installed version

18. Install Spanish Acquisition

    1. Get it by running:

          git clone git://github.com/ghwatson/SpanishAcquisitionIQC.git

       This places the source code repository at /home/jonathan/SpanishAcquisitionIQC/.
    2. From the SpanishAcquisitionIQC directory, run `sudo python setup.py install`
    3. Copy the example apps to another directory (eg. ~/spacq_apps)
    4. Build the offline docs with `make -C docs html`

19. Create desktop shortcuts ("launchers"):

    * Application:

      * Acquisition -> /home/jonathan/spacq-apps/acquisition.py
      * Data Explorer -> /home/jonathan/spacq-apps/data_explorer.py

    * Location:

      * Instructions -> /home/jonathan/instructions
      * Spanish Acquisition Documentation -> http://ghwatson.github.com/SpanishAcquisitionIQC/docs/
      * Spanish Acquisition Documentation (Offline) -> file:///home/jonathan/SpanishAcquisitionIQC/docs/_build/html/index.html
