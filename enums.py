from enum import Enum


class BossNames(Enum):
    drake = {'Antharas': (18, 22,  7), 'Valakas': (18, 22, 7)}
    simple_apik = {'Orfen': (18, 22,  3), 'Beleth': (18, 22, 5), 'Baium': (18, 22, 4), 'Core': 0,
                   'Queen Ant': (18, 22, 2)}

    @classmethod
    def s_apic(cls):
        return list(cls.drake.value.keys())

    @classmethod
    def s_apic_l(cls):
        return cls.drake.value

    @classmethod
    def apic(cls):
        return list(cls.simple_apik.value.keys())

    @classmethod
    def apic_l(cls):
        return cls.simple_apik.value

    @classmethod
    def apic_drake_l(cls):
        return cls.drake.value


class SubscribeFilds(Enum):
    subid = 0
    userid = 1
    bosid = 2
    not_1h = 3
    not_30m = 4
    not_15m = 5
    not_5m = 6
    server = 7


class SubscribeFilds_3rb(Enum):
    subid = 0
    userid = 1
    timekill = 2
    bossname = 3
    not_1h = 4
    not_30m = 5
    not_15m = 6
    not_5m = 7
    server = 8


class Forts(Enum):
    allfortslist = ['Aaru Fortress', 'Archaic Fortress', 'Demon Fortress', 'Dragonspine Fortress',
                    'Hive Fortress', 'Ivory Fortress', 'Monastic Fortress', 'Narsell Fortress',
                    'Shanty Fortress', 'Tanor Fortress', 'White Sands Fortress', 'Antharas Fortress',
                    'Bayou Fortress', 'Borderland Fortress', 'Cloud Mountain Fortress',
                    'Floran Fortress', 'Hunters Fortress', 'Swamp Fortress', 'Southern Fortress',
                    'Valley Fortress', 'Western Fortress']


class Castle(Enum):
    allcastllit = ['Gludio', 'Dion', 'Giran', 'Oren', 'Aden', 'Innadril', 'Goddard', 'Rune', 'Schuttgart']


class ParseURL(Enum):
    prime_x1 = {'Fort': "https://asterios.tm/static/ratings/fortress/3.html?1661275879208",
                'Boss': "https://asterios.tm/index.php?cmd=rss&serv=3&filter=all",
                'Castle': "https://asterios.tm/static/ratings/castles/3/0.html?1661333833305"}
    asterios_x5 = {'Fort': "https://asterios.tm/static/ratings/fortress/0.html?1661421142205",
                   'Boss': "https://asterios.tm/index.php?cmd=rss&serv=1&filter=all",
                   'Castle': "https://asterios.tm/static/ratings/castles/index0.html?1661421262158"}
    hunter_x55 = {'Fort': "https://asterios.tm/static/ratings/fortress/2.html",
                  'Boss': "https://asterios.tm/index.php?cmd=rss&serv=2&filter=all",
                  'Castle': "https://asterios.tm/static/ratings/castles/2/0.html"}
    media_x3 = {'Fort': "https://asterios.tm/static/ratings/fortress/6.html",
                'Boss': "https://asterios.tm/index.php?cmd=rss&serv=6&filter=all",
                'Castle': "https://asterios.tm/static/ratings/castles/6/0.html"}

    @classmethod
    def servers(cls):
        return list(i.name for i in cls)


class ServersStatus(Enum):
    server_list = ['prime_x1', 'asterios_x5', 'hunter_x55', 'media_x3']
    url_status = "https://asterios.tm/static/status.html"
    # Fort = "https://asterios.tm/static/ratings/fortress/3.html?1661275879208"
    # Boss = "https://asterios.tm/index.php?cmd=rss&serv=3&filter=all"
    # Castle = "https://asterios.tm/static/ratings/castles/3/0.html?1661333833305"
