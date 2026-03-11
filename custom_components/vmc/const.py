"""Costanti VMC."""

DOMAIN = "vmc"

CONF_HOST = "host"
CONF_PORT = "port"
CONF_SLAVE_ID = "slave_id"

SENSOR_TYPES = {
    "velocita_selezionata": {
        "name": "Velocità selezionata",
        "icon": "mdi:speedometer",
        "unit": None,
        "device_class": None,
        "address": 0
    },
    "velocita_attiva": {
        "name": "Velocità attiva",
        "icon": "mdi:fan",
        "unit": None,
        "device_class": None,
        "address": 1
    },
    "modalita_gestione": {
        "name": "Modalità gestione",
        "icon": "mdi:air-conditioner",
        "unit": None,
        "device_class": None,
        "address": 7
    },
    "temp_immissione": {
        "name": "Temp immissione",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "device_class": "temperature",
        "address": 26
    }
    # Aggiungi altri...
}

MODALITA_MAP = {
    0: "OFF",
    1: "Ventilazione",
    2: "Deumidifica",
    3: "Integrazione",
    4: "Deum+Integ",
    5: "Ricircolo",
    6: "Vent+Deum",
    7: "Vent+Integ",
    8: "Vent+Deu+Int",
    9: "Vent+Ricircolo",
    10: "Manutenzione",
    11: "Stand-By",
    12: "Deum STBY",
    13: "Integ STBY",
    14: "Deum+Integ STBY",
    15: "Vent+Deum STBY",
    16: "Vent+Integ STBY",
    17: "Vent+Deu+Int STBY"
}
