#Raspberry PI - Licht Alarmanlage

1. Anschluss/Verkabelung PI 1b

+=====+========+===============+
| PIN | Raspi  | BH1750/GY-302 |
+=====+========+===============+
| SDA | GPIO 4 | SDA           |
+-----+--------+---------------+
| SCL | GPIO 4 | SCL           |
+-----+--------+---------------+
| VCC | GPIO 4 | VCC           |
+-----+--------+---------------+
| GND | GPIO 4 | GND           |
+-----+--------+---------------+


**Hinweis**: Auslesen des PI Modeltyps (Shell):
cat /sys/firmware/devicetree/base/model



2.  i2c Interface aktivieren

raspi-config nonint do_i2c 0

3. apt install -y python3-smbus i2c-tools
oder pip install smbus2

