Demonstration of IEEE P21451-1-6 for 2018 IEEE IES IECON PlugFest
====

IEEE P21451-1-6 Working Group (WG) Development Meeting on STANDARD FOR A SMART TRANSDUCER INTERFACE FOR SENSORS, ACTUATORS AND DEVICES – MESSAGE QUEUE TELEMETRY TRANSPORT (MQTT)FOR NETWORKED DEVICE COMMUNICATION. 

IEEE P21451-1-6 is included in IEEE 1451 Standards family. An event, IEEE 1451 Standards Plug Fest, is achieved at INTEROP 1451, IECON '18. The objectives are as follows.

- Provide the IEEE 1451/21451 standards community with verification and validation platforms for the standards so the community can test the development of their applications to these benchmarks, ensuring compliance and interoperability to their systems.
- The standards and platforms will provide compliance and interoperability to the IoT applications and its industrial components (IIoT)
- Encourage industry partners to make sure of the verification and validation platforms for IEEE Standards compliance in the industry context.
- Verification and developing platforms are being implemented following several different approaches, allowing coverage of specific sensor transducer applications conforming to the IEEE P1451 standards.
- The goal of these platforms is to support users with “turn-key” approaches for their applications, by providing relatively easy initial start-up processes, allowing easy installation and configuration.

This demonstration program shows the typical example of IEEE P21451-1-6.

## Requirement

Required libraries python packages must be installed. Follow the description of Install section.
You may use BLE-based Smart IoT Sensor Module manufactured by ALPS ELEC Co.Ltd. If you don’t have the module, you can use pseudo sensor mode. TIM and NCAP are run on Raspberry-Pi 3 or BLE/Bluetooth compatible Raspberry-Pi. NOOBS+Raspbian installation is recommended. For the minimum, two raspberry-pi, one for TIM and the other for NCAP are required. Designed NCAP has a capability of multiple connections and supports multiple TIM.

To compile and execute MQTTnet-based MQTT server, Microsoft Visual Studio is required.

## Installation
### MQTTnet Server
- On windows 10 machine, extract GitHub image by using GitHub client for Windows or compatible GitHub clients.
- Click PlugFestUWP/PlugFest.sln
Then, Visual Studio opens the design, and you can compile and execute the program.
- When you execute the server, you may see a window with some buttons. A few buttons of functions are implemented.
You can execute MQTTnet server by pressing “Start MQTT Server” button.

### Confiture and establish Raspberry Pi Environment
#### Raspberry Pi Setup
KEIO-MODEL Installation manual for Raspberry-Pi 3 (B+)

(Notice) It is easy to copy the installation-completed image. However, we have a problem in creating images. Still, it is easy to mount the image and copy into your installation.

- This installation requires >16G MicroSD memory. 8G is not enough.
- Install NOOBS. If you have a kit, it is Ok, but in many cases, it uses 8G SD memory.
- Follow general installation guide of NOOBS.
- Edit your /boot/config.txt for fitting your display.

+ If you use Getic mobile display panel, then give a pache as follows.

```
	disable_oberscan=1
	overscan_left=-
	overscan_top=0
	#framebuffer_width=1920
	#framebuffer_height=1080
	framebuffer_width=1366
	framebuffer_height=768
	hdmi_group=1
	hdmi_mode=16
```

+ if you use 7-inch touch panel for Raspberry-Pi, add the following setting at the tail of the file.

```
	lcd_lotate=2
```

You will install software keyboard by using the following command after this installation.

```
	# apt-get install matchbox-keyboard
```

- Update your environment

To update use the following commands.

```
	# apt-get -y upgrade
	# apt-get -y update
	# apt-get -y dist-upgrade
```

We need a Japanese environment. You can skip here. Here is for our lab members.
Install the following languages adding to “C.”

```
	# raspi-config ($ means root command line)
		C.UTF-8
		en_US.UTF-8
		ja_JP.UTF-8
			Set default language to en_US
	# apt-get -y install fonts-noto
	# apt-get -y install uim uim-anthy
	# reboot
```

- Dnsutils

Install dnsutils. It is convenient for checking network conectivity.

```
	# apt-get install dnsutils
```

- You may set up your network environment here. You may finish the network environment setting in your installation.

- Install VNC and enable sshd for remote connection
VNC and sshd are standard method for Raspberry Pi for remote connection.

```
	# raspi-config
```

Then select memnu to enable the following services.

```
	ssh enable
	vnc enable
```

From here, it is better to use rloing for installing multiple machines.  Login via ssh clients (the best one is rlogin)

```
	# apt-get install realvnc-vnc-server (may be not required if use raspi-config)
```

- Add USB serial cable entry to use USB serial cable for connecting Serial devices if you want.
dtoverlay=pi3-miniuart-bt

- ALPS ELEC Smart IoT BLE Sensor Module
 If you don’t have the module, you can skip this installation. In this case, you will use a dummy sensor module, which generates random values.

Blog of TomoSoft (as given below) explains how to install the ALPS module. This is a very simple way for us to connect sensors to Raspberry Pi via Bluetooth.
http://tomosoft.jp/design/?p=8104
http://www.hiramine.com/physicalcomputing/raspberrypi3/wlan_howto.html
These pages are written in Japanese. Use google translator. Simply, it is enough to follow the process below.

- Connect to the Internet
Firstly, it is better to check the update.

```
	# sudu su (This is not a good way? Yes, but is easy.)
	# apt-get update (Anytime you do something, you should do update.)
```

- Set time
Fix the clock of your raspberry pi.

```
	# apt-get install ntpdate # (we need time for getting sensor data. We want to store sensor data with time.)
	# timedatectl set-timezone Asia/Tokyo # (select your timezone)
	# ntpdate ntp.nict.jp # (select your closest ntp server)
	# systemctl enable ssh
```

- Install required modules.
Firstly, blupy, a python interface to communicate via bluetooth

```
	# apt-get install python-pip libglib2.0-dev
	# apt-get install git build-essential
	# cd
	# pip install bluepy
```

+ we need some part of bluepy sourses. Extract sources from git.
+ our working directory is /export/
In the working directory, install bluepy.

```
	# mkdir /export/install
	# cd /export/install
	# git clone https://github.com/IanHarvey/bluepy.git
	# cd bluepy
```

Maybe, it is needless but we want to update the blupy.

```
	# python setup.py build
	# python setup.py install
	# cd bluepy
	# ls btle.py (check the existence of the file)
	# cd /export/install
```

+ download our design
Our all design is available in GitHub.

```
	# git clone https://github.com/westlab/PlugFest
	# cd /export/install/bluepy/bluepy
	# cp ../../PlugFest/PlugFestRP/alps/alps_sensor.py .
	# python alps_sensor.py
```

Check it does not report any errors, and just quiet.
Type Ctrl-C

```
	# ls 
```

Check btle.pyc and bluepy-helper.
These files are very important to communicate with the Bluetooth sensor module.

```
	# cd /export
	# ln -s install/PlugFest/PlugFestRP/alps .
	# cp install/bluepy/bluepy/{btle.pyc,bluepy-helper} alps
	# cd alps
	# python alps_sensor.py
```

Type Ctrl-C
Check it does not report any errors, and just quiet, again

```
	# apt-get install vim (you may edit the source file)
```

The source is also given at the end of this file.

Edit the following line in the source to fit your sensor module address.
alps = AlpsSensor("28:A1:83:E1:59:48")
The address is printed on the surface of the sensor module.

```
	# python alps_sensor.py
```

Then you can get the sensor values. It takes about 10 seconds when it executes.
The program uses HyblidMode and set all sensors ON.
The sampling rate of the acceleration sensor and the geomagnetic sensor is 100 mil seconds.
Others are 1 second.
The following code has a fix of sign handling mistakes in the original source. Acceleration sensor value and geomagnetic sensor value are signed values. The original code handles these values as unsigned values.

#### MQTT clients and server installation.

Docker version and general version are available.
Ok, then, let’s do both. (Wao!)

- MQTT broker server on Docker

Install docker by following commands.

```
	# apt-get update
	# curl -sSL https://get.docker.com | sh
```

This is only what you do. However, it takes time.

To execute docker container by pi adding to root.

You may have some troubles when resolving DNS of get.docker.com or getting PGP keys. In this case, IP address and the canonical name of get.docker.com by using nslookup command, and directly write the address and name to /etc/hosts. You also add download.docker.com to the hosts file.

If you edited /etc/hosts, bring it back.

```
	# usermod -aG docker pi
```

As a test, execute hypriot image. This hypriot is a very nice site, which preparing manyu kinesof Docker images.

```
	# docker run -d -p 80:80 hypriot/rpi-busybox-httpd
```

This command executes httpd web server in a docker. Check a test site is open in your raspberry-pi by accessing a web browser in your network.

```
	# docker ps
	# docker stop [NAME] (This name will be changed at any time)
```

Then install docker image of mosquitto MQTT server

```
	# docker run -tip 1883:1883 -p 9001:9001 pascaldevink/rpi-mosquitto
```

If you execute mosquitto docker image by changing its configurations, do following commands.

```
	mkdir -p /srv/mqtt/config/
	mkdir -p /srv/mqtt/data/
	mkdir -p /srv/mqtt/log/
```

place your mosquitto.conf in /srv/mqtt/config/

NOTE: You have to change the permissions of the directories to allow the user to read/write to data and log and read from config directory For TESTING purposes you can use the following command

```
	# chmod -R 777 /srv/mqtt/*
	# docker run -ti -p 1883:1883 -p 9001:9001 \
	-v /srv/mqtt/config:/mqtt/config:ro \
	-v /srv/mqtt/log:/mqtt/log \
	-v /srv/mqtt/data/:/mqtt/data/ \
	--name mqtt pascaldevink/rpi-mosquitto
```

- Mosquitto MQTT broker installation

Install mosquitto MQTT broker server. It is very popular.

```
	# apt install mosquitto
	# apt install mosquitto-clients (MQTT clients)
```

To confirm the installation and execution, do following commands.

```
	# mosquitto_sub -d -t orz
	# mosquitto_pub -d -t orz -m hogehoge
```

To connect another host, use –h option.

You may also install MQTT server into Windows 10 machine.
http://www.eclipse.org/downloads/download.php?file=/mosquitto/binary/win32/mosquitto-1.4.14-install-win32.exe

You may also install the following libraries.
From [ http://slproweb.com/products/Win32OpenSSL.html ], download [ install Win32OpenSSL_Light-1_0_2k.exe ] and execute it.
Copy libeay32.dll and ssleay32.dll in C:¥OpenSSL-Win32¥bin of OpenSSL to C:\Program Files (x86)\mosquitto
Get pthreadVC2.dll from ftp://sources.redhat.com/pub/pthreads-win32/dll-latest/dll/x86/
And, copy it to C:\Program Files (x86)\mosquitto

If you want to execute Mosquitto Broker, it only can be executed as a Windows service.
Use Services menu of Windows Management tool and enable it.

- Windows 10 mosquitto clients

Check your config file

```
	C:\Program Files (x86)\mosquitto\mosquitto.conf
	>cd "C:\Program Files (x86)\mosquitto"
	>mosquito_sub –t test
```

In another window

```
	>cd "C:\Program Files (x86)\mosquitto"
	>mosquito_pub –t test –m hoge
```

It shows “hoge”.

You may change your Firewall configuration. Check system and security menu in control panel.
And change the mosuquitto.exe, mosquitt_pub.exe,mosquitto_sub.exe as public functions.

One important point. Windows mosquitto cannot send and recive UTF coded messages. This is a serious problem.

To use MQTT server from python, install paho-mqtt.
This is only available for Python v3.
So you may change python link to python 3. In my environment, it is not required.

```
	# cd /usr/bin
	# rm python
	# ln -s python3.5 python
```

Do not forget restoring this change.
Install the paho library.

```
	# pip install paho-mqtt
```

pub-, sub- client examples of paho-mqtt are as follows.
You can check it in /export/install/PlugFest/PlugFestRP/mqtt-client-py

```
	# cd /export
	# ln -s install/PlugFest/PlugFestRP/mqtt-client-py
```

Check the operation of paho-mqtt.

#### Installing Bluetooth connection

- Two raspberry-pi are required to check the connectivity.
- This model supports multiple clients. Here, we use three raspberry-pi to check the operation.

- Preparation
Firstly, you should do this.

```
	# apt-get update
	# apt-get upgrade
	# apt-get dist-upgrade
```

If you do not have our environment, execute the following command.

```
	# mkdir –p /export/install
	# cd /export/install
	# git clonse https://github.com/westlab/PlugFest
	# cd /export
	# ln -s install/PlugFest/PlugFestRP/bluetooth-com .
	# ln -s install/PlugFest/PlugFestRP/TEDS .
```

- Install Bluetooth driver 
get bluetooth repository.

```
	# apt-get install bluetooth
```

- Install concerning packages
get the following repositories.

```
	# apt-get install libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev libdbus-glib-1-dev
```

- Install python library (bluez)
Install bluz library.

```
	# apt-get install python-dev
	# apt-get install libboost-python-dev libglib2.0 libboost-thread-dev
	# apt-get install libbluetooth3-dev
	# cd /export/install
	# wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.50.tar.xz
	# xz -dv bluez-5.50.tar.xz
	# tar -xf bluez-5.50.tar
	# cd bluez-5.50/
	# ./configure --enable-experimental
	# make –j 3 (you can use 4 cores for compile. It will be very heavy. This compile process will take comparatively longer time than others.)
	# make install
	# pip install pybluez
```

- Install GUI interfaces for bluetooth
Update Bluetooth control icon on the menu.

```
	# apt-get install pi-bluetooth blueman
```

Default GUI Bluetooth on the menu bar will be overwrited.

If you want, you can install the following modles to connect Bluetooth speaker.

```
	# apt-get install pulseaudio pavucontrol pulseaudio-module-bluetooth 
	# apt-get install bluez-hcidump
```

Now, reboot your system. Need reboot to use new GUI.

```
	# reboot
```

Remove old Bluetooth GUI interface on the menu
Click the right button of the mouse on the old Bluetooth icon on the menu -> Select Remove “Bluetooth” From Panel

- Additional installation to use bluetooth
Edit /lib/systemd/system/bluetooth.service

```
	#ExecStart=/usr/lib/bluetooth/bluetoothd –C
	ExecStart=/usr/local/libexec/bluetooth/bluetoothd -C
	ExecStartPost=/usr/bin/sdptool add SP
```

Then execute pip to install gittlib.

```
	# pip install gattlib (this will take a while)
```

If you failed in installing gattlib, you have to install it from source.

```
	# cd /export/install
	# pip3 download gattlib
	# tar xvzf ./gattlib-0.20150805.tar.gz
	# cd gattlib-0.20150805/
	# sed -ie 's/boost_python-py34/boost_python-py35/' setup.py
	# pip3 install . (Do not miss the last period)
```

- Reload daemon process
Now reload the daemon processes.

```
	# systemctl daemon-reload
	# systemctl restart bluetooth
```

## Usage

### Pairing
This paring task is sometimes tough because you do not see terget Bluetooth device in your window or list. You may try again and again to type commands to make pair.

As a preparation, give appropriate Bluetooth name to client and server machine.
[GUI]
Select Adapter -> select discoverable anytime
Select Adapter -> give name

Firstly, check the physical address of Bluetooth device on Raspberry Pi.
Now you have to select NCAP (server) and TIM (client).
Check the server’s physical address.
Type the following commands in the server.

```
	# hciconfig
	hci0:   Type: BR/EDR  Bus: USB
	    BD Address: B8:27:EB:9A:A4:C7 ACL MTU: 1021:8  SCO MTU: 64:1
	    UP RUNNING PSCAN 
	    RX bytes:1724 acl:0 sco:0 events:92 errors:0
	    TX bytes:1364 acl:0 sco:0 commands:87 errors:0
```

This “BD Address: B8:27:EB:9A:A4:C” is the physical address of the bluetooth module.

We have two method to pair Bluetooth devices. One is GUI-based operation the other is command-line-based operation. 

+ Give a permission to be searched from others server

[CMD]

```
	# bluetoothctl
	Agent registered
	[bluetooth] # power on               <= command
	Changing power on succeeded
	[bluetooth] # discoverable on         <= command
	Changing discoverable on succeesed
	[CHG] Controller B8:27:EB:9A:A4:C7 Discoverable : yes
```

You can leave from bluetoothctl by using quit command.

- Pairing from client
Pair with client. You will check the blutooth physical address of server.

```
	#bluetoothctl
	Agent registered
	[bluetooth] # pair B8:27:EB:9A:A4:C7
	Attempting to pair with B8:27:EB:9A:A4:C7   <= success
	Device B8:27:EB:9A:A4:C7 not available      <= fail. Try again and again
```

[GUI]
Click Bluetooth icon on the menu bar.
Select Make Discoverable
Click Devices
Find server physical address
Click the address and select pair

It is better to check the Bluetooth connection by transferring file via Bluetooth menu interface.

If pairing made a success, you may see a cross mark on the address list.

### Execution
#### Windows MQTTnet Server
Open PlugFestUWP/PlugFest.sln in GitHub directory.
Press "Start MQTT Server".

#### Raspberry Pi
Now you can execute a program.

```
	# cd /export/install/bluetooth-com
	# cp /export/install/bluepy/bluepy/{btle.pyc,bluepy-helper} .
```

[server]

```
	# python rfcommserver.py –h
```

Now just run it. (No MQTT server connection)

```
	# python rfcommserver.py -v
```

[client]

```
	# python alps.py –h
```

You may special ALPS IOT Module address by –m option, or you may use pseudo_sensor option to use random values. As an example:

```
	# python alps.py -P -d B8:27:EB:DB:97:2F -v
```

### Paring trouble shooting

- To check all physical addresses in command line

```
	#hciconfig –a
		50 BD Address: B8:27:EB:35:5A:5E
		51 BD Address: B8:27:EB:DB:D2:8E
		52 BD Address: B8:27:EB:72:B3:11
		53 BD Address: B8:27:EB:E3:BC:BE
		54 BD Address: B8:27:EB:9A:A4:C7
		55 BD Address: B8:27:EB:3E:00:C5
```

- Check rfcomm operation
You have to set up two machines; server and client.
Client
Make /dev/rfcomm0

```
	# rfcomm bind 0 B8:27:EB:9A:A4:C7
```

Server

```
	# rfcomm watch 0 1 agetty rfcomm0 115200 linux -a pi
```

Then, execute the following command at client. You will login to the server machine via Bluetooth.

```
	# screen /dev/rfcomm0 115200
```

This means your rfcomm is open and works correctly.
If it does not work, you may reset devices and confirm it.

```
	# rfcom release [n] /dev/rfcomm[n]
	# systemctl restart Bluetooth
```

By using GUI you can confirm the status of Bluetooth device.

```
	# hciconfig hci0 up
	# sdptool add SP
	# sdptool browse local | grep -i serial

	# sdptool add –channel=[n]
	# rfcomm bind [n] B8:27:EB:9A:A4:C7     This [n] should be changed independently.

	# ls -la /dev/rfcomm*
		crw-rw---- 1 root dialout 216, 1  Sep  23 21:10 /dev/rfcomm1
	# ls -la /var/lib/bluetooth
		drwx------  4 root root 4096  Sep  23 20:50 B8:27:EB:72:B3:11 (address of yourself)
```

### Application

#### Node-RED
Elasticsearch+kibana works but is very heavy.
Dashing is Ok but is just a “dashboard”

Here, install Node-red as IoT application.

```
	# apt-get install –y nodered
	# systemctl start nodered
```

Access to the following site.
http://localhost:1880
localhost is your installed machine name or IP address.

It has many functions to connect IoT services.
One important function for demonstration is drawing graphs.
Install nodered-dashboard

```
	# systemctl stop nodered
	# apt-get install npm
	# update-nodejs-and-nodered
	# npm i node-red-dashboard
	# systemctl start nodered
```

To use dashboard, select menu button (right top) and select “setting”, “pallet”, and search node-red-dashboard. Then press install button on the node-red-dashboard tab. You may find many plugin applications for Node-RED.

You can access the dashboard panel by the following URL.
http://localhost:1880/ui

It does not have authorization as it’s original configuration.
It is better to install authorization function for Node-RED.

```
	# npm i bcrypt
```

You have to implement encoded password into the configuration file.
Use the following command to get the encoded password.

```
	# node -e "console.log(require('bcryptjs').hashSync(process.argv[1], 8));" PASSWORD
```

Type the code into setting.js

```
	# vi ~pi/node-red/settings.js
```

Edit the appropriate section of the file as follows.

```
adminAuth: {
    type: "credentials",
    users: [{
        username: "admin",
        password: "$2a$08$zZWtXTja0fB1pzD4sHCMyOCMYz2Z6dNbM6tl8sJogENOMcxWV9DN.",
        permissions: "*"
    }]
}
```

#### Prevent Darkout
If you want to use the dashboard like KIOSK, which means to prevent the screen darkout, use the following command.

```
	$ xset s 0 0
	$ xset s noblank
	$ set s noexpose
	$ xset dpms 0 0 0
```

You may think these commands are automatically executed. Then, edit the following file.

```
	$ vi ~pi/.config/lxsession/LXDE-pi/autostart
```

Then, insert the following lines to the end of the file.

```
@xset s 0 0
@xset s noblank
@xset s noexpose
@xset dpms 0 0 0
```

The screen will not go sleep.
