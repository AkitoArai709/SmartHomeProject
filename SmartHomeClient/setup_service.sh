cp /home/pi/SmartHomeProject/SmartHomeClient/smart-home-client.service /etc/systemd/system/
systemctl daemon-reload 
systemctl enable smart-home-client.service
systemctl start smart-home-client.service