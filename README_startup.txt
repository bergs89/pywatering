How to run at startup:
edit  sudo nano /lib/systemd/system/pywatering.service :
------
[Unit]
 Description=PyWatering Service
 After=multi-user.target

 [Service]
 Type=idle
 ExecStart=/usr/bin/python3 /home/pi/Projects/pywatering/main.py > /var/log/pywatering.log 2>&1

 [Install]
 WantedBy=multi-user.target

-----

sudo chmod 644 /lib/systemd/system/pywatering.service
sudo systemctl daemon-reload
sudo systemctl enable pywatering.service

edit  sudo nano /lib/systemd/system/pywatering_stop_button.service :
------
[Unit]
 Description=PyWatering_stop_button Service
 After=multi-user.target

 [Service]
 Type=idle
 ExecStart=sudo /usr/bin/python3 /home/pi/Projects/pywatering/stop_button.py > /var/log/pywatering_stop.log 2>&1

 [Install]
 WantedBy=multi-user.target

 --------

sudo chmod 644 /lib/systemd/system/pywatering_stop_button.service
sudo systemctl daemon-reload
sudo systemctl enable pywatering_stop_button.service
sudo reboot
