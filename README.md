# Raspberry PI - Licht Alarmanlage

## Allgemein

Das Projekt dient als "Alarmanlage" welche mittels Lichtsensor (siehe Handware) getriggert wird.
Sollte es in dem eingesetzen Raum hell werden (Lichtschwelle überschritten), wird eine Nachricht an eine Telegram Gruppe versandt.
Der Alarm wird nur alle n Minuten ausgelöst.

**Hardware:**
- GY-302 BH1750 Lichtsensor (I2C)
- Raspberry

## Anschluss/Verkabelung

***Raspberry PI Model B Rev 2***
```
+=====+================+===============+
| PIN | Raspberry      | BH1750/GY-302 |
+=====+================+===============+
| SDA | GPIO 2 / PIN 3 | SDA           |
+-----+----------------+---------------+
| SCL | GPIO 3 / PIN 5 | SCL           |
+-----+----------------+---------------+
| VCC | GND            | VCC           |
+-----+----------------+---------------+
| GND | VCC (5V)       | GND           |
+-----+----------------+---------------+
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
```
***Alternative:***
```
pip install smbus
pip install smbus2
pip3 install smbus
pip3 install smbus2
```
