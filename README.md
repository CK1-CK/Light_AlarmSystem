# Raspberry PI - Licht Alarmanlage

## Anschluss/Verkabelung PI 1b

```
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
```

**Hinweis**: Auslesen des PI Modeltyps (Shell):
cat /sys/firmware/devicetree/base/model


## Installationsvoraussetzungen

### i2c Interface aktivieren
```
raspi-config nonint do_i2c 0
```

### i2c Module installieren
```
apt install -y python3-smbus i2c-tools
***Alternative:***
pip install smbus2
```
