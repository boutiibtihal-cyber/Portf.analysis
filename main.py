from flask import Flask, render_template, request, jsonify, session, Response
import pandas as pd, numpy as np, requests, json, re, base64, warnings, secrets, time
from scipy import stats
from datetime import datetime, timedelta
warnings.filterwarnings("ignore")
try: requests.packages.urllib3.disable_warnings()
except: pass

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
USERNAME, PASSWORD = "trader", "albarid2024"
LOGO_B64 = "/9j/4AAQSkZJRgABAQAASABIAAD/4QBMRXhpZgAATU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAACkKADAAQAAAABAAABcQAAAAD/7QA4UGhvdG9zaG9wIDMuMAA4QklNBAQAAAAAAAA4QklNBCUAAAAAABDUHYzZjwCyBOmACZjs+EJ+/8AAEQgBcQKQAwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/bAEMAAQEBAQEBAgEBAgMCAgIDBAMDAwMEBgQEBAQEBgcGBgYGBgYHBwcHBwcHBwgICAgICAkJCQkJCwsLCwsLCwsLC//bAEMBAgICAwMDBQMDBQsIBggLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLC//dAAQAKf/aAAwDAQACEQMRAD8A/v4ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP/Q/v4ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP/R/v4ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP/S/v4ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP/T/v4ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP/U/v4ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP/V/v4ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP/W/v4ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAormfFHinw74J8P3fizxdfw6bpdhE01xdXDrHFDGv8TM3Svy78Qf8ABaH9ibQvEDaFbXmr6pEjbDe2lj/o/wDvfvGjk/8AHKmU4x3ZpClOfwK5+tVFeIfBX4+fCX9orwcnjj4O63BrWnltkjRbllif+5JG21429mAr2+mmmrohpp2YUUUUxBRRXy/+0x+1V8Iv2UfAb+NvinqAiZwyWdhEQ11eSrztij6n/ab7qd6TaSuyoxcnZLU9a+InxK8FfCPwffePfiLqUOk6NpyGW4ubltqqP6sf4VWvn39kD9onVv2p/C+t/GGy086b4TuNSez0BJkxc3EFr8sl1J6eZJ8qp/Bs5r+UL9pv9rz47ft8/FXTPD1wj29hcXiWmh6BA7eWss7eXHu/56Ttu+83Ff2PfAT4VaN8Cfg54b+EOhYMGgWEVrvX/lrIq/vJP+2j7m/GsoVeeVo7HVXw6pQXP8T/AAPZ6KKK2OMKKKKACiiigD//1/7+KKKKACiiigAooooAKKKKACivm348/tXfAH9mjTYb34y+I7bR3uULQWx3S3Mqr1Kwxq0hUf3tuK5v9nD9tT9nf9qq71HSvgtrLaheaUiS3UEtvNbyJG52q2JFXIJ9Knnje19S/Zy5eazt36H1tRRX5f8A/BRX/goJoH7IXg3/AIRjwi8N9481eI/YbVsMlrG3y/aZlHYH/Vp/GfaiU1FXYU6cpyUY7n6Naf4o8PaxrGoaDpl3FcXulPGl5Cj7ngaVd8Ycfw7l+YV01fht/wAEP/FGv+NPhf8AEXxb4svJtR1PUvEaz3V1cPvllle3RmZmr9yaIS5oqQ61Pkm4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WvbyjJ5YuXPUkoUlvJu3yXmZHxe+M1/4+un0jSd8Okq/A/ilx3bp/wB814RX1z4Z/ZU1SQLJ4q1FYV/55QDc3/fRr6N8LfBz4e+EQraZp6yTJ0lm/eN+Zr+Qv+ID+IfHGYyzniaosO5veo7yUekYUo35UukZOPd63Z97/rPlWW0Vh8GnO3bb1bfX5H5/eFvhV478XhZtJsWSE8+bJ+7j/wDHq+ofCf7Lei6eFuPF141+4H+qi/dx/n96vrqiv6H4N+jHwjkrjWx0Hi6y61Pgv5U1pbym5nymYcZY/E3jTfs4+W/3v9LHNeH/AA/onh+1+w6FaxWkOPuxrtFdLRRX9CYbDUcPTjRoQUYRVkopJJdklZJHyk5yk3KTu331CiiityQooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP/R/v4ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA5S+8NaDql1FqOo2sdxLFyjSDdt+gNdXRRXPRwtGlKdSnBKUtZNJJya0u2t/K+y0KlOUkk3otgoooroJCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA//0v7+KKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD/0/7+KKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD/1P7+KKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD/1f7+KKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD/1v7+KKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD/2Q=="

# ══════════════════════════════════════════════════════════════════════════════
#  BASE ISIN — 78 valeurs MASI
# ══════════════════════════════════════════════════════════════════════════════
ISIN_DB = {
 "MA0000012445":{"nom":"ATTIJARIWAFA BANK",           "ticker":"ATW",  "secteur":"Banques",              "prix":477.95,"roe":15.2,"roa":1.4,"per":14.2,"div":17.0,"beta":0.82,"vol":12.1},
 "MA0000012312":{"nom":"SODEP-Marsa Maroc",            "ticker":"MSA",  "secteur":"Transport & Logistique","prix":245.00,"roe":19.2,"roa":8.4,"per":17.2,"div":9.8, "beta":0.65,"vol":10.1},
 "MA0000011488":{"nom":"ITISSALAT AL-MAGHRIB",         "ticker":"IAM",  "secteur":"Télécommunications",   "prix":130.10,"roe":38.5,"roa":12.4,"per":18.3,"div":7.6,"beta":0.55,"vol":8.9},
 "MA0000011058":{"nom":"MANAGEM",                      "ticker":"MNG",  "secteur":"Mines & Métaux",       "prix":1720.0,"roe":18.4,"roa":8.7,"per":22.1,"div":48.0,"beta":1.15,"vol":18.3},
 "MA0000012320":{"nom":"LafargeHolcim Maroc",          "ticker":"LHM",  "secteur":"BTP & Ciments",        "prix":1919.0,"roe":22.1,"roa":10.2,"per":20.5,"div":78.5,"beta":0.78,"vol":14.2},
 "MA0000012528":{"nom":"TGCC S.A",                     "ticker":"TGCC", "secteur":"BTP & Ciments",        "prix":185.00,"roe":14.5,"roa":6.2,"per":18.5,"div":5.0, "beta":0.90,"vol":16.0},
 "MA0000012437":{"nom":"BANK OF AFRICA",               "ticker":"BOA",  "secteur":"Banques",              "prix":198.00,"roe":10.5,"roa":0.9,"per":11.5,"div":6.3, "beta":0.71,"vol":13.2},
 "MA0000012783":{"nom":"SGTM S.A",                     "ticker":"SGTM", "secteur":"BTP & Ciments",        "prix":320.00,"roe":12.0,"roa":5.5,"per":15.0,"div":4.0, "beta":0.85,"vol":15.0},
 "MA0000010506":{"nom":"CIMENTS DU MAROC",             "ticker":"CMA",  "secteur":"BTP & Ciments",        "prix":1650.0,"roe":19.8,"roa":9.1,"per":18.7,"div":64.0,"beta":0.72,"vol":13.5},
 "MA0000011884":{"nom":"BCP",                          "ticker":"BCP",  "secteur":"Banques",              "prix":268.00,"roe":12.8,"roa":1.1,"per":12.8,"div":10.0,"beta":0.75,"vol":11.3},
 "MA0000012585":{"nom":"AKDITAL",                      "ticker":"AKD",  "secteur":"Santé",                "prix":485.00,"roe":19.5,"roa":8.8,"per":25.5,"div":5.8, "beta":0.75,"vol":13.1},
 "MA0000012205":{"nom":"TAQA MOROCCO",                 "ticker":"TAQA", "secteur":"Énergie & Pétrole",    "prix":1180.0,"roe":22.0,"roa":8.5,"per":14.0,"div":25.0,"beta":0.70,"vol":11.5},
 "MA0000012627":{"nom":"CFG BANK",                     "ticker":"CFG",  "secteur":"Banques",              "prix":52.00, "roe":9.5, "roa":0.8,"per":12.0,"div":3.0, "beta":0.68,"vol":12.0},
 "MA0000012247":{"nom":"COSUMAR",                      "ticker":"CSR",  "secteur":"Agroalimentaire",      "prix":305.00,"roe":21.5,"roa":9.8,"per":16.4,"div":13.7,"beta":0.62,"vol":9.8},
 "MA0000011801":{"nom":"LABEL VIE",                    "ticker":"LBV",  "secteur":"Distribution",         "prix":2850.0,"roe":16.8,"roa":5.9,"per":20.8,"div":71.2,"beta":0.62,"vol":10.2},
 "MA0000011512":{"nom":"DOUJA PROM ADDOHA",            "ticker":"ADH",  "secteur":"Immobilier",           "prix":42.50, "roe":5.1, "roa":1.8,"per":8.9, "div":1.0, "beta":1.25,"vol":22.5},
 "MA0000011819":{"nom":"ALLIANCES",                    "ticker":"ALL",  "secteur":"Immobilier",           "prix":38.00, "roe":4.5, "roa":1.5,"per":12.0,"div":0.0, "beta":1.20,"vol":24.0},
 "MA0000010951":{"nom":"AFRIQUIA GAZ",                 "ticker":"GAZ",  "secteur":"Énergie & Pétrole",    "prix":4200.0,"roe":22.8,"roa":9.5,"per":16.7,"div":200.0,"beta":0.82,"vol":12.1},
 "MA0000010928":{"nom":"WAFA ASSURANCE",               "ticker":"WAA",  "secteur":"Assurances",           "prix":4050.0,"roe":17.9,"roa":3.2,"per":13.8,"div":180.0,"beta":0.60,"vol":9.2},
 "MA0000011454":{"nom":"CIH BANK",                     "ticker":"CIH",  "secteur":"Banques",              "prix":320.00,"roe":11.2,"roa":1.0,"per":13.1,"div":11.2,"beta":0.68,"vol":10.8},
 "MA0000012460":{"nom":"ARADEI CAPITAL",               "ticker":"ARAD", "secteur":"Immobilier",           "prix":380.00,"roe":8.2, "roa":3.5,"per":15.2,"div":18.2,"beta":0.55,"vol":8.9},
 "MA0000012080":{"nom":"JET CONTRACTORS",              "ticker":"JET",  "secteur":"BTP & Ciments",        "prix":195.00,"roe":13.0,"roa":5.8,"per":14.0,"div":3.5, "beta":0.92,"vol":16.5},
 "MA0000012718":{"nom":"CMGP GROUP",                   "ticker":"CMGP", "secteur":"Distribution",         "prix":480.00,"roe":15.0,"roa":7.0,"per":17.0,"div":8.0, "beta":0.80,"vol":13.0},
 "MA0000010019":{"nom":"SONASID",                      "ticker":"SCE",  "secteur":"BTP & Ciments",        "prix":550.00,"roe":8.2, "roa":4.1,"per":12.3,"div":14.0,"beta":0.88,"vol":15.1},
 "MA0000010381":{"nom":"CREDIT DU MAROC",              "ticker":"CDM",  "secteur":"Banques",              "prix":580.00,"roe":9.8, "roa":0.8,"per":10.9,"div":17.0,"beta":0.65,"vol":9.7},
 "MA0000012619":{"nom":"HPS",                          "ticker":"HPS",  "secteur":"Technologies",         "prix":5800.0,"roe":22.8,"roa":14.5,"per":28.5,"div":121.0,"beta":0.85,"vol":14.8},
 "MA0000011793":{"nom":"MINIERE TOUISSIT",             "ticker":"CMT",  "secteur":"Mines & Métaux",       "prix":1900.0,"roe":20.1,"roa":11.2,"per":17.8,"div":60.0,"beta":1.12,"vol":16.8},
 "MA0000012031":{"nom":"LESIEUR CRISTAL",              "ticker":"LES",  "secteur":"Agroalimentaire",      "prix":175.00,"roe":14.8,"roa":6.5,"per":14.2,"div":7.2, "beta":0.58,"vol":8.7},
 "MA0000012262":{"nom":"TOTALENERGIES MARKETING MAROC","ticker":"TQM",  "secteur":"Énergie & Pétrole",    "prix":1350.0,"roe":25.2,"roa":10.8,"per":15.3,"div":68.5,"beta":0.88,"vol":13.4},
 "MA0000012502":{"nom":"SOTHEMA",                      "ticker":"SOT",  "secteur":"Chimie & Pharma",      "prix":1580.0,"roe":18.5,"roa":8.2,"per":19.3,"div":44.3,"beta":0.68,"vol":11.2},
 "MA0000012239":{"nom":"RESIDENCES DAR SAADA",         "ticker":"RDS",  "secteur":"Immobilier",           "prix":56.00, "roe":6.3, "roa":2.1,"per":9.8, "div":2.0, "beta":1.18,"vol":20.8},
 "MA0000011850":{"nom":"DELTA HOLDING",                "ticker":"DHO",  "secteur":"Conglomérats",         "prix":42.00, "roe":9.5, "roa":4.2,"per":11.5,"div":1.3, "beta":0.75,"vol":12.5},
 "MA0000012395":{"nom":"MUTANDIS SCA",                 "ticker":"MUT",  "secteur":"Agroalimentaire",      "prix":198.00,"roe":13.5,"roa":6.1,"per":13.8,"div":5.8, "beta":0.55,"vol":8.2},
 "MA0000010068":{"nom":"SMI",                          "ticker":"SMI",  "secteur":"Mines & Métaux",       "prix":1450.0,"roe":16.2,"roa":7.9,"per":19.5,"div":37.0,"beta":1.08,"vol":17.1},
 "MA0000012759":{"nom":"VICENNE",                      "ticker":"VIC",  "secteur":"Distribution",         "prix":120.00,"roe":11.0,"roa":5.0,"per":14.0,"div":3.0, "beta":0.80,"vol":14.0},
 "MA0000011710":{"nom":"ATLANTASANAD",                 "ticker":"ATL",  "secteur":"Assurances",           "prix":175.00,"roe":14.2,"roa":2.8,"per":12.1,"div":6.7, "beta":0.55,"vol":8.5},
 "MA0000010811":{"nom":"BMCI",                         "ticker":"BMCI", "secteur":"Banques",              "prix":650.00,"roe":10.1,"roa":0.9,"per":11.8,"div":22.0,"beta":0.70,"vol":10.5},
 "MA0000012767":{"nom":"CASH PLUS S.A",                "ticker":"CASH", "secteur":"Services Financiers",  "prix":85.00, "roe":15.0,"roa":6.5,"per":18.0,"div":4.0, "beta":0.75,"vol":13.0},
 "MA0000010365":{"nom":"SOCIETE DES BOISSONS DU MAROC","ticker":"SBM",  "secteur":"Agroalimentaire",      "prix":3100.0,"roe":28.3,"roa":12.1,"per":24.6,"div":165.0,"beta":0.45,"vol":7.5},
 "MA0000010969":{"nom":"AUTO HALL",                    "ticker":"AUTO", "secteur":"Distribution",         "prix":98.00, "roe":12.5,"roa":5.1,"per":12.5,"div":3.7, "beta":0.70,"vol":11.5},
 "MA0000012007":{"nom":"SANLAM MAROC",                 "ticker":"SAH",  "secteur":"Assurances",           "prix":110.00,"roe":13.0,"roa":2.5,"per":11.5,"div":8.5, "beta":0.58,"vol":9.0},
 "MA0000011462":{"nom":"RISMA",                        "ticker":"RIS",  "secteur":"Tourisme & Hôtellerie","prix":68.00, "roe":7.0, "roa":2.5,"per":18.0,"div":0.0, "beta":1.10,"vol":19.0},
 "MA0000012163":{"nom":"MICRODATA",                    "ticker":"MIC",  "secteur":"Technologies",         "prix":320.00,"roe":12.0,"roa":6.5,"per":15.0,"div":3.5, "beta":0.70,"vol":12.0},
 "MA0000011637":{"nom":"DISWAY",                       "ticker":"DWY",  "secteur":"Technologies",         "prix":580.00,"roe":18.0,"roa":9.5,"per":16.0,"div":12.0,"beta":0.78,"vol":13.5},
 "MA0000012387":{"nom":"IMMORENTE INVEST",             "ticker":"IMR",  "secteur":"Immobilier",           "prix":105.00,"roe":6.5, "roa":3.0,"per":14.0,"div":4.0, "beta":0.50,"vol":8.0},
 "MA0000011744":{"nom":"SALAFIN",                      "ticker":"SAF",  "secteur":"Services Financiers",  "prix":850.00,"roe":14.0,"roa":2.5,"per":11.0,"div":12.0,"beta":0.65,"vol":10.5},
 "MA0000012296":{"nom":"AFMA",                         "ticker":"AFM",  "secteur":"Services Financiers",  "prix":2000.0,"roe":22.0,"roa":10.0,"per":14.0,"div":45.0,"beta":0.60,"vol":9.5},
 "MA0000011934":{"nom":"COLORADO",                     "ticker":"COL",  "secteur":"Chimie & Pharma",      "prix":68.00, "roe":18.0,"roa":8.5,"per":15.0,"div":4.5, "beta":0.72,"vol":11.5},
 "MA0000010944":{"nom":"AGMA",                         "ticker":"AGM",  "secteur":"Services Financiers",  "prix":2200.0,"roe":25.0,"roa":12.0,"per":12.0,"div":55.0,"beta":0.55,"vol":8.5},
 "MA0000010357":{"nom":"EQDOM",                        "ticker":"EQD",  "secteur":"Services Financiers",  "prix":820.00,"roe":13.5,"roa":2.2,"per":10.5,"div":28.0,"beta":0.65,"vol":10.0},
 "MA0000011728":{"nom":"SNEP",                         "ticker":"SNP",  "secteur":"Chimie & Pharma",      "prix":780.00,"roe":16.8,"roa":7.9,"per":14.6,"div":22.0,"beta":0.72,"vol":11.8},
 "MA0000011421":{"nom":"DARI COUSPATE",                "ticker":"DAR",  "secteur":"Agroalimentaire",      "prix":3200.0,"roe":20.0,"roa":9.5,"per":18.0,"div":12.0,"beta":0.58,"vol":9.5},
 "MA0000012023":{"nom":"UNIMER",                       "ticker":"UNI",  "secteur":"Agroalimentaire",      "prix":140.00,"roe":12.1,"roa":5.4,"per":13.1,"div":5.2, "beta":0.55,"vol":8.2},
 "MA0000010415":{"nom":"OULMES",                       "ticker":"OUL",  "secteur":"Agroalimentaire",      "prix":1420.0,"roe":13.8,"roa":6.2,"per":18.2,"div":36.0,"beta":0.52,"vol":8.5},
 "MA0000010936":{"nom":"ALUMINIUM DU MAROC",           "ticker":"ALM",  "secteur":"Industrie",            "prix":1250.0,"roe":14.5,"roa":7.8,"per":16.8,"div":48.0,"beta":0.80,"vol":13.2},
 "MA0000011942":{"nom":"ENNAKL",                       "ticker":"ENK",  "secteur":"Distribution",         "prix":48.00, "roe":10.0,"roa":4.5,"per":12.0,"div":3.5, "beta":0.75,"vol":12.5},
 "MA0000012536":{"nom":"DISTY TECHNOLOGIES",           "ticker":"DST",  "secteur":"Technologies",         "prix":380.00,"roe":15.0,"roa":8.0,"per":16.0,"div":4.0, "beta":0.82,"vol":14.0},
 "MA0000011009":{"nom":"AUTO NEJMA",                   "ticker":"ANJ",  "secteur":"Distribution",         "prix":720.00,"roe":11.0,"roa":5.0,"per":13.0,"div":4.0, "beta":0.72,"vol":12.0},
 "MA0000010340":{"nom":"WAFA ASSURANCE (ord.)",        "ticker":"WAA",  "secteur":"Assurances",           "prix":4050.0,"roe":17.9,"roa":3.2,"per":13.8,"div":180.0,"beta":0.60,"vol":9.2},
 "MA0000011587":{"nom":"FENIE BROSSETTE",              "ticker":"FNI",  "secteur":"Industrie",            "prix":185.00,"roe":10.5,"roa":5.0,"per":12.0,"div":5.0, "beta":0.78,"vol":13.0},
 "MA0000011215":{"nom":"MAGHREBAIL",                   "ticker":"MGB",  "secteur":"Services Financiers",  "prix":420.00,"roe":12.0,"roa":2.0,"per":10.0,"div":15.0,"beta":0.62,"vol":10.0},
 "MA0000012700":{"nom":"STOKVIS NORD AFRIQUE",         "ticker":"SVS",  "secteur":"Distribution",         "prix":48.00, "roe":9.0, "roa":4.0,"per":11.0,"div":3.0, "beta":0.80,"vol":14.0},
 "MA0000011660":{"nom":"PROMOPHARM S.A.",              "ticker":"PRO",  "secteur":"Chimie & Pharma",      "prix":1350.0,"roe":22.0,"roa":10.5,"per":17.0,"div":18.0,"beta":0.65,"vol":10.5},
 "MA0000012106":{"nom":"S.M MONETIQUE",                "ticker":"SMO",  "secteur":"Technologies",         "prix":380.00,"roe":18.0,"roa":9.0,"per":15.0,"div":6.0, "beta":0.78,"vol":13.0},
 "MA0000011678":{"nom":"M2M GROUP",                    "ticker":"M2M",  "secteur":"Technologies",         "prix":520.00,"roe":18.5,"roa":10.2,"per":22.1,"div":9.3, "beta":0.92,"vol":15.5},
 "MA0000010035":{"nom":"MAROC LEASING",                "ticker":"MRL",  "secteur":"Services Financiers",  "prix":280.00,"roe":11.0,"roa":1.8,"per":9.5, "div":8.0, "beta":0.68,"vol":11.0},
 "MA0000012056":{"nom":"STROC INDUSTRIE",              "ticker":"STR",  "secteur":"Industrie",            "prix":38.00, "roe":8.0, "roa":3.5,"per":14.0,"div":2.0, "beta":0.90,"vol":16.0},
 "MA0000011991":{"nom":"BALIMA",                       "ticker":"BAL",  "secteur":"Assurances",           "prix":160.00,"roe":9.0, "roa":1.8,"per":10.0,"div":12.0,"beta":0.58,"vol":9.0},
 "MA0000012114":{"nom":"AFRIC INDUSTRIES SA",          "ticker":"AFI",  "secteur":"Industrie",            "prix":320.00,"roe":10.0,"roa":4.5,"per":12.0,"div":3.0, "beta":0.82,"vol":14.0},
 "MA0000010985":{"nom":"MAGHREB OXYGENE",              "ticker":"MOX",  "secteur":"Chimie & Pharma",      "prix":520.00,"roe":12.0,"roa":5.5,"per":13.0,"div":14.0,"beta":0.70,"vol":11.5},
 "MA0000011868":{"nom":"CARTIER SAADA",                "ticker":"CTS",  "secteur":"Agroalimentaire",      "prix":55.00, "roe":8.5, "roa":4.0,"per":14.0,"div":2.5, "beta":0.65,"vol":11.0},
 "MA0000012593":{"nom":"MED PAPER",                    "ticker":"MEP",  "secteur":"Industrie",            "prix":28.00, "roe":7.0, "roa":3.0,"per":12.0,"div":1.5, "beta":0.88,"vol":15.5},
 "MA0000011595":{"nom":"REALISATIONS MECANIQUES",      "ticker":"RMX",  "secteur":"Industrie",            "prix":285.00,"roe":9.5, "roa":4.5,"per":11.0,"div":4.0, "beta":0.85,"vol":14.5},
 "MA0000011579":{"nom":"INVOLYS",                      "ticker":"INV",  "secteur":"Technologies",         "prix":350.00,"roe":14.0,"roa":7.0,"per":14.0,"div":5.0, "beta":0.75,"vol":12.5},
 "MA0000012551":{"nom":"DELATTRE LEVIVIER MAROC",      "ticker":"DLM",  "secteur":"Industrie",            "prix":92.00, "roe":8.0, "roa":3.5,"per":13.0,"div":2.0, "beta":0.88,"vol":15.0},
 "MA0000010571":{"nom":"ZELLIDJA S.A",                 "ticker":"ZLD",  "secteur":"Mines & Métaux",       "prix":245.00,"roe":6.0, "roa":3.0,"per":18.0,"div":0.0, "beta":1.05,"vol":18.0},
 "MA0000011132":{"nom":"IB MAROC.COM",                 "ticker":"IBM",  "secteur":"Technologies",         "prix":42.00, "roe":10.0,"roa":5.0,"per":13.0,"div":2.0, "beta":0.80,"vol":14.0},
 "MA0000010993":{"nom":"REBAB COMPANY",                "ticker":"REB",  "secteur":"Industrie",            "prix":22.00, "roe":8.0, "roa":3.5,"per":12.0,"div":1.5, "beta":0.85,"vol":14.5},
}

TICKER_TO_ISIN = {v["ticker"]:k for k,v in ISIN_DB.items()}
NOM_TO_ISIN    = {v["nom"].lower():k for k,v in ISIN_DB.items()}
ALL_TICKERS    = sorted(set(v["ticker"] for v in ISIN_DB.values()))

def resolve_isin(raw):
    raw = str(raw).strip()
    up  = raw.upper()
    if up in ISIN_DB: return up
    if up in TICKER_TO_ISIN: return TICKER_TO_ISIN[up]
    rl = raw.lower()
    if rl in NOM_TO_ISIN: return NOM_TO_ISIN[rl]
    for nom_l,isin in NOM_TO_ISIN.items():
        if rl in nom_l or nom_l in rl: return isin
    return None

# ══════════════════════════════════════════════════════════════════════════════
#  BVC LIVE COURS
# ══════════════════════════════════════════════════════════════════════════════
_LIVE = {"data":{}, "ts":0}
_TTL  = 1800

BVC_H = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/142",
    "Accept":"application/json, text/html, */*",
    "Accept-Language":"fr-FR,fr;q=0.9",
}

def _build_id():
    try:
        r = requests.get("https://www.casablanca-bourse.com/fr", headers=BVC_H, verify=False, timeout=15)
        m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', r.text)
        if m: return json.loads(m.group(1)).get("buildId")
    except: pass
    return None

def _fetch_all_bvc():
    try:
        r = requests.get(
            "https://www.casablanca-bourse.com/api/proxy/fr/api/bourse/dashboard/ticker",
            params={"marche":59,"class[]":50}, headers=BVC_H, verify=False, timeout=15)
        if r.status_code != 200: return {}
        out = {}
        for v in r.json().get("data",{}).get("values",[]):
            tk  = str(v.get("ticker","")).strip().upper()
            if not tk: continue
            px  = float(v.get("field_cours_courant") or v.get("field_closing_price") or 0)
            var = float(v.get("field_var_veille") or 0)
            hau = float(v.get("field_high_price") or 0)
            bas = float(v.get("field_low_price")  or 0)
            ouv = float(v.get("field_opening_price") or 0)
            ref = float(v.get("field_static_reference_price") or px)
            vol = float(v.get("field_cumul_volume_echange") or 0)
            if px > 0:
                out[tk] = {"prix":round(px,2),"var":round(var,2),
                           "haut":round(hau,2),"bas":round(bas,2),
                           "ouv":round(ouv,2),"ref":round(ref,2),
                           "vol":round(vol,0),"source":"BVC Live",
                           "date":datetime.now().strftime("%d/%m/%Y")}
        return out
    except: return {}

def get_live():
    now = time.time()
    if now - _LIVE["ts"] > _TTL or not _LIVE["data"]:
        fresh = _fetch_all_bvc()
        if fresh: _LIVE["data"]=fresh; _LIVE["ts"]=now
    return _LIVE["data"]

def get_info(raw_id):
    isin = resolve_isin(raw_id)
    if not isin:
        return {"ticker":str(raw_id).upper(),"nom":str(raw_id),"secteur":"Inconnu",
                "isin":"—","prix":0,"var":None,"haut":None,"bas":None,"ouv":None,
                "ref":None,"vol":None,"roe":None,"roa":None,"per":None,"div":None,
                "beta":1.0,"vol_hist":15.0,"source":"Inconnu","date":"—"}
    base = dict(ISIN_DB[isin])
    base.update({"isin":isin,"vol_hist":base.pop("vol",15.0),
                 "var":None,"haut":None,"bas":None,"ouv":None,"ref":None,"vol":None,
                 "source":"Statique BVC","date":"Référence"})
    live = get_live()
    tk   = base["ticker"]
    if tk in live:
        lv = live[tk]
        base.update({k:lv[k] for k in ["prix","var","haut","bas","ouv","ref","vol","source","date"]})
    return base

# ══════════════════════════════════════════════════════════════════════════════
#  SIGNAL ACHAT / VENTE basé sur données BVC + analyse technique
# ══════════════════════════════════════════════════════════════════════════════
def generer_signal(info, sr):
    """
    Génère un signal BUY / SELL / HOLD basé sur :
    - Position du prix vs support/résistance du jour
    - Variation J-1
    - Ratios fondamentaux (PER, ROE)
    - Momentum (prix vs référence)
    Retourne dict avec signal, score, raisons, analyse
    """
    prix  = info.get("prix") or 0
    var   = info.get("var")  or 0
    per   = info.get("per")  or 0
    roe   = info.get("roe")  or 0
    roa   = info.get("roa")  or 0
    beta  = info.get("beta") or 1.0
    haut  = sr.get("haut_j") or (prix * 1.012)
    bas   = sr.get("bas_j")  or (prix * 0.988)
    ref   = sr.get("ref_j")  or prix
    sup   = sr.get("support") or bas
    res   = sr.get("resistance") or haut
    pivot = sr.get("pivot")  or prix

    score  = 0
    raisons_achat  = []
    raisons_vente  = []
    raisons_neutre = []

    # 1. Position prix vs support/résistance intrajournalier
    spread = res - sup
    if spread > 0:
        pos_rel = (prix - sup) / spread  # 0=sur support, 1=sur résistance
        if pos_rel < 0.25:
            score += 2
            raisons_achat.append(f"Prix proche du support journalier ({sup} MAD) — zone d'achat potentielle")
        elif pos_rel > 0.80:
            score -= 2
            raisons_vente.append(f"Prix proche de la résistance journalière ({res} MAD) — zone de prise de profit")
        else:
            raisons_neutre.append(f"Prix en zone neutre entre support ({sup}) et résistance ({res})")

    # 2. Variation J-1
    if var > 2.0:
        score -= 1
        raisons_vente.append(f"Forte hausse J-1 ({var:+.2f}%) — risque de correction à court terme")
    elif var > 0.5:
        score += 1
        raisons_achat.append(f"Momentum positif J-1 ({var:+.2f}%)")
    elif var < -2.0:
        score += 1
        raisons_achat.append(f"Baisse significative J-1 ({var:+.2f}%) — opportunité d'entrée potentielle")
    elif var < -0.5:
        score -= 1
        raisons_vente.append(f"Tendance baissière J-1 ({var:+.2f}%)")
    else:
        raisons_neutre.append(f"Variation faible ({var:+.2f}%) — marché neutre")

    # 3. Valorisation (PER)
    if per > 0:
        if per < 12:
            score += 2
            raisons_achat.append(f"PER attractif à {per}x — valeur potentiellement sous-évaluée")
        elif per > 28:
            score -= 1
            raisons_vente.append(f"PER élevé à {per}x — valorisation tendue")
        elif per < 18:
            score += 1
            raisons_achat.append(f"PER raisonnable à {per}x")
        else:
            raisons_neutre.append(f"PER de {per}x — valorisation dans la moyenne sectorielle")

    # 4. ROE / ROA (qualité)
    if roe > 20:
        score += 2
        raisons_achat.append(f"ROE excellent à {roe}% — forte rentabilité des fonds propres")
    elif roe > 12:
        score += 1
        raisons_achat.append(f"ROE solide à {roe}%")
    elif roe < 6:
        score -= 1
        raisons_vente.append(f"ROE faible à {roe}% — rentabilité insuffisante")

    if roa > 8:
        score += 1
        raisons_achat.append(f"ROA de {roa}% — bonne efficacité des actifs")

    # 5. Bêta / risque
    if beta > 1.3:
        raisons_neutre.append(f"Bêta élevé ({beta:.2f}) — valeur volatile, risque accru")
    elif beta < 0.6:
        raisons_achat.append(f"Bêta défensif ({beta:.2f}) — faible corrélation au marché")

    # 6. Prix vs référence du jour
    if ref > 0 and prix > 0:
        diff_ref = (prix - ref) / ref * 100
        if diff_ref < -1.5:
            score += 1
            raisons_achat.append(f"Prix sous le cours de référence ({diff_ref:+.1f}%) — dynamique d'achat")
        elif diff_ref > 1.5:
            score -= 1
            raisons_vente.append(f"Prix au-dessus du cours de référence ({diff_ref:+.1f}%) — dynamique de vente")

    # Décision finale
    if score >= 3:
        signal="BUY"; couleur="vert"
    elif score <= -2:
        signal="SELL"; couleur="rouge"
    else:
        signal="HOLD"; couleur="orange"

    # Analyse narrative
    toutes = raisons_achat + raisons_neutre + raisons_vente
    analyse = f"Sur la base des données de marché du jour, le score technique/fondamental est de {score:+d}. "
    if signal == "BUY":
        analyse += f"Les signaux sont majoritairement positifs. Points forts : {'; '.join(raisons_achat[:2])}."
        if raisons_vente: analyse += f" Points de vigilance : {'; '.join(raisons_vente[:1])}."
        conseil = "Achat recommandé. Placer un stop-loss sous le support journalier."
    elif signal == "SELL":
        analyse += f"Les signaux indiquent une pression vendeuse. Points faibles : {'; '.join(raisons_vente[:2])}."
        if raisons_achat: analyse += f" Facteurs favorables : {'; '.join(raisons_achat[:1])}."
        conseil = "Prise de profit ou réduction de position recommandée."
    else:
        analyse += f"Situation mixte. {'; '.join(toutes[:2])}."
        conseil = "Maintien de la position recommandé. Attendre une confirmation directionnelle."

    return {
        "signal":  signal,
        "score":   score,
        "couleur": couleur,
        "conseil": conseil,
        "analyse": analyse,
        "raisons_achat":  raisons_achat,
        "raisons_vente":  raisons_vente,
        "raisons_neutre": raisons_neutre,
    }

# ══════════════════════════════════════════════════════════════════════════════
#  SUPPORT / RÉSISTANCE INTRADAY réels depuis BVC
# ══════════════════════════════════════════════════════════════════════════════
def get_sr_intraday(ticker, prix_ref):
    live = get_live()
    lv   = live.get(ticker.upper(),{})
    haut = lv.get("haut") or 0
    bas  = lv.get("bas")  or 0
    ouv  = lv.get("ouv")  or prix_ref
    ref  = lv.get("ref")  or prix_ref
    source = "BVC Intraday"
    if haut <= 0 or bas <= 0:
        vol_j = prix_ref * 0.012
        haut  = round(prix_ref + vol_j, 2)
        bas   = round(prix_ref - vol_j, 2)
        source= "Estimé (vol. ±1.2%)"
    pivot = round((haut + bas + ref) / 3, 2)
    r1    = round(2*pivot - bas, 2)
    r2    = round(pivot + (haut-bas), 2)
    s1    = round(2*pivot - haut, 2)
    s2    = round(pivot - (haut-bas), 2)
    return {
        "support":    round(bas, 2),
        "resistance": round(haut, 2),
        "pivot":      pivot,
        "r1":r1,"r2":r2,"s1":s1,"s2":s2,
        "haut_j":     round(haut,2),
        "bas_j":      round(bas,2),
        "ouv_j":      round(ouv,2),
        "ref_j":      round(ref,2),
        "source_sr":  source,
    }

# ══════════════════════════════════════════════════════════════════════════════
#  CALCULS FINANCIERS PORTEFEUILLE
# ══════════════════════════════════════════════════════════════════════════════
def _rend(info, n=252):
    b = float(info.get("beta",1.0) or 1.0)
    v = float(info.get("vol_hist",15.0)) / 100 / np.sqrt(252)
    rm = np.random.normal(0.0003, 0.009, n)
    return b*rm + np.random.normal(0,v,n), rm

def calc_risque(rp_arr, rm_arr, vt):
    rp=pd.Series(rp_arr); rm=pd.Series(rm_arr)
    v95=float(np.percentile(rp,5)); v99=float(np.percentile(rp,1))
    q95=rp[rp<=v95]; e95=float(q95.mean()) if len(q95)>0 else v95
    q99=rp[rp<=v99]; e99=float(q99.mean()) if len(q99)>0 else v99
    std=rp.std(); rf=0.03/252
    sh  =float((rp.mean()-rf)/std*np.sqrt(252)) if std>0 else 0
    neg =rp[rp<0]; so=float((rp.mean()-rf)/neg.std()*np.sqrt(252)) if len(neg)>1 and neg.std()>0 else 0
    cum =(1+rp).cumprod(); pic=cum.cummax(); mdd=float(((cum-pic)/pic).min())
    cov =np.cov(rp_arr,rm_arr); beta=float(cov[0,1]/cov[1,1]) if cov[1,1]!=0 else 1
    vol_a=float(std*np.sqrt(252)*100)
    te   =float((rp-rm).std()*np.sqrt(252)*100)
    ir_v =float((rp-rm).mean()/(rp-rm).std()*np.sqrt(252)) if (rp-rm).std()>0 else 0
    cal  =float(rp.mean()*252/abs(mdd)) if mdd!=0 else 0
    alpha=float((rp.mean()-beta*rm.mean())*252*100)
    ret_a=float(rp.mean()*252*100)
    return dict(
        var95=round(abs(v95*vt),2),var99=round(abs(v99*vt),2),
        es95=round(abs(e95*vt),2),es99=round(abs(e99*vt),2),
        var95_pct=round(abs(v95)*100,3),
        var95_p=round(abs(float(stats.norm.ppf(0.05,rp.mean(),std))*vt),2),
        sharpe=round(sh,3),sortino=round(so,3),calmar=round(cal,3),
        treynor=round(float((rp.mean()-rf)*252/beta)*100 if beta!=0 else 0,4),
        mdd=round(mdd*100,2),beta=round(beta,3),alpha=round(alpha,3),
        vol=round(vol_a,2),te=round(te,2),ir=round(ir_v,3),
        skew=round(float(stats.skew(rp)),3),kurt=round(float(stats.kurtosis(rp)),3),
        ret_ann=round(ret_a,2),
    )

def traiter(df):
    df.columns=[str(c).strip().lower() for c in df.columns]
    MAP={
        "id": ["titre","ticker","valeur","action","code","symbole","instrument","code isin","isin","stock"],
        "qte":["quantité","quantite","qté","qte","nombre","nb titres","qty","shares"],
        "pa": ["prix achat","prixachat","coût","cout","prix d'achat","pa","prix_achat",
               "prix de revient","prx achat","purchase price","prix d achat"],
    }
    def col(k):
        for c in MAP[k]:
            if c in df.columns: return c
        return None
    ci=col("id"); cq=col("qte"); cp=col("pa")
    if not ci: raise ValueError("Colonne identifiant introuvable (Titre, Code ISIN, Ticker…)")
    if not cq: raise ValueError("Colonne Quantité introuvable")
    if not cp: raise ValueError("Colonne Prix Achat introuvable")
    df[cq]=pd.to_numeric(df[cq],errors="coerce").fillna(0)
    df[cp]=pd.to_numeric(df[cp],errors="coerce").fillna(0)
    infos=[get_info(str(r[ci])) for _,r in df.iterrows()]
    for k in ["nom","ticker","secteur","isin","prix","var","haut","bas","ouv","roe","roa","per","div","beta","vol_hist","source","date"]:
        df["_"+k]=[i.get(k) for i in infos]
    df["_vm"]=df["_prix"]*df[cq]; df["_va"]=df[cp]*df[cq]
    df["_pnl"]=df["_vm"]-df["_va"]
    df["_pct"]=((df["_prix"]-df[cp])/df[cp].replace(0,np.nan)*100).fillna(0)
    vt=df["_vm"].sum(); ct=df["_va"].sum()
    df["_w"]=df["_vm"]/vt if vt>0 else 0
    pnl_t=df["_pnl"].sum(); pnl_pct=pnl_t/ct*100 if ct>0 else 0
    np.random.seed(42); n=252
    rm_base=np.random.normal(0.0003,0.009,n); rp_arr=np.zeros(n)
    for _,row in df.iterrows():
        b=float(row.get("_beta") or 1.0); v=float(row.get("_vol_hist") or 15.0)/100/np.sqrt(252)
        rp_arr += (b*rm_base+np.random.normal(0,v,n))*float(row["_w"])
    risque=calc_risque(rp_arr,rm_base,vt)
    live_n=sum(1 for i in infos if i.get("source")=="BVC Live")
    sec=df.groupby("_secteur")["_vm"].sum().reset_index()
    sec["pct"]=(sec["_vm"]/vt*100).round(1)
    sec=sec.rename(columns={"_secteur":"secteur","_vm":"valeur"})
    sec=sec.sort_values("pct",ascending=False).to_dict("records")
    rp=pd.Series(rp_arr); rm=pd.Series(rm_base)
    hist_y,edges=np.histogram(rp,bins=30)
    v95_raw=float(np.percentile(rp,5))
    dist=[{"x":round(float((edges[i]+edges[i+1])/2)*100,3),"y":int(c),
           "queue":bool((edges[i]+edges[i+1])/2<=v95_raw)} for i,c in enumerate(hist_y)]
    cum_p=((1+rp).cumprod()-1)*100; cum_m=((1+rm).cumprod()-1)*100
    cum=[{"j":i+1,"p":round(float(p),3),"m":round(float(m),3)} for i,(p,m) in enumerate(zip(cum_p,cum_m))]
    titres=[]
    for _,row in df.iterrows():
        b=float(row.get("_beta") or 1.0)
        titres.append({
            "ticker":str(row["_ticker"]).upper(),"nom":row["_nom"],"secteur":row["_secteur"],
            "isin":row["_isin"],"qte":int(row[cq]),"pa":round(float(row[cp]),2),
            "prix":round(float(row["_prix"]),2),"vm":round(float(row["_vm"]),2),
            "pnl":round(float(row["_pnl"]),2),"pct":round(float(row["_pct"]),2),
            "poids":round(float(row["_w"])*100,2),
            "roe":row["_roe"],"roa":row["_roa"],"per":row["_per"],"div":row["_div"],"beta":round(b,2),
            "var":round(float(row["_var"]),2) if row["_var"] is not None else None,
            "haut":row["_haut"],"bas":row["_bas"],"source":row["_source"],"date":row["_date"],
        })
    return {"resume":{"valeur":round(vt,2),"cout":round(ct,2),"pnl":round(pnl_t,2),
                      "pnl_pct":round(pnl_pct,2),"n":len(df),"ret_ann":risque["ret_ann"],"live_n":live_n},
            "risque":risque,"secteurs":sec,"titres":titres,"dist":dist,"cum":cum,
            "beta_port":risque["beta"],"vt":round(vt,2)}

def demo_data():
    d=pd.DataFrame({
        "Code ISIN":  ["MA0000012445","MA0000011488","MA0000012320","MA0000011058",
                       "MA0000012247","MA0000011884","MA0000012262","MA0000010928",
                       "MA0000010506","MA0000012437"],
        "Quantité":   [200,500,50,100,300,150,80,30,60,400],
        "Prix Achat": [420,118,1750,1580,270,240,1200,3800,1500,175],
    })
    return traiter(d)

# ══════════════════════════════════════════════════════════════════════════════
#  ROUTES FLASK
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/")
def index():
    if not session.get("ok"): return render_template("login.html")
    return render_template("dashboard.html")

@app.route("/logo")
def logo():
    return Response(base64.b64decode(LOGO_B64), mimetype="image/png")

@app.route("/connexion", methods=["POST"])
def connexion():
    d=request.get_json()
    if d.get("utilisateur")==USERNAME and d.get("motdepasse")==PASSWORD:
        session["ok"]=True; return jsonify({"ok":True})
    return jsonify({"ok":False,"erreur":"Identifiants incorrects"}),401

@app.route("/deconnexion")
def deconnexion():
    session.clear(); return ("",204)

@app.route("/upload", methods=["POST"])
def upload():
    if not session.get("ok"): return jsonify({"erreur":"Non authentifié"}),401
    f=request.files.get("fichier")
    if not f: return jsonify({"erreur":"Aucun fichier"}),400
    try:
        df=pd.read_excel(f)
        if df.empty: return jsonify({"erreur":"Fichier vide"}),400
        return jsonify(traiter(df))
    except ValueError as e: return jsonify({"erreur":str(e)}),422
    except Exception as e:  return jsonify({"erreur":f"Erreur: {e}"}),500

@app.route("/demo")
def demo():
    if not session.get("ok"): return jsonify({"erreur":"Non authentifié"}),401
    return jsonify(demo_data())

@app.route("/refresh-cours")
def refresh_cours():
    if not session.get("ok"): return jsonify({"erreur":"Non authentifié"}),401
    _LIVE["ts"]=0; live=get_live()
    return jsonify({"ok":True,"n":len(live)})

@app.route("/valeur/<isin>")
def detail_valeur(isin):
    if not session.get("ok"): return jsonify({"erreur":"Non authentifié"}),401
    info     = get_info(isin)
    prix_ref = info.get("prix") or 100.0
    ticker   = info.get("ticker","")
    # Intraday S/R
    sr = get_sr_intraday(ticker, prix_ref)
    # Signal
    sig = generer_signal(info, sr)
    # Risk individuel
    np.random.seed(hash(isin)%10000); n=252
    ri_arr,rm_arr = _rend({"beta":info.get("beta",1),"vol_hist":info.get("vol_hist",15)})
    ri=pd.Series(ri_arr); rm=pd.Series(rm_arr)
    v95=float(np.percentile(ri,5))
    dpa=info.get("div") or 0
    rend_div=round(dpa/prix_ref*100,2) if prix_ref>0 else 0
    cov=np.cov(ri_arr,rm_arr)
    beta_ind=float(cov[0,1]/cov[1,1]) if cov[1,1]!=0 else 1.0
    return jsonify({
        "info":info,"sr":sr,"signal":sig,
        "dpa":dpa,"rend_div":rend_div,
        "var95":round(abs(v95*prix_ref),2),
        "sharpe":round(float((ri.mean()-0.03/252)/ri.std()*np.sqrt(252)),3) if ri.std()>0 else 0,
        "beta":round(beta_ind,3),"vol_ann":round(float(ri.std()*np.sqrt(252)*100),2),
        "perf_ytd":round(float(ri_arr.sum()*100),2),
    })

@app.route("/search-valeur")
def search_valeur():
    """Recherche d\'une valeur par ticker, ISIN ou nom pour l\'ajout au portefeuille."""
    if not session.get("ok"): return jsonify({"erreur":"Non authentifié"}),401
    q = request.args.get("q","").strip()
    if len(q) < 2: return jsonify({"resultats":[]})
    ql = q.lower(); qu = q.upper()
    resultats=[]
    for isin,info in ISIN_DB.items():
        nom=info["nom"]; ticker=info["ticker"]
        if (qu in ticker or ql in nom.lower() or qu in isin or
            ticker.startswith(qu) or nom.lower().startswith(ql)):
            resultats.append({"isin":isin,"ticker":ticker,"nom":nom,
                               "secteur":info["secteur"],"prix":info["prix"]})
    resultats.sort(key=lambda x: (not x["ticker"].startswith(qu), x["ticker"]))
    return jsonify({"resultats":resultats[:8]})

@app.route("/valeur-info/<isin>")
def valeur_info(isin):
    """Retourne les infos de base d\'une valeur pour l\'ajout au portefeuille."""
    if not session.get("ok"): return jsonify({"erreur":"Non authentifié"}),401
    info = get_info(isin)
    return jsonify({"ok":True,"info":info})

@app.route("/simuler-masi", methods=["POST"])
def simuler_masi():
    if not session.get("ok"): return jsonify({"erreur":"Non authentifié"}),401
    d=request.get_json()
    titres=d.get("titres",[]); var_masi=float(d.get("var_masi",0))/100; vt=float(d.get("vt",0))
    resultats=[]; nouvelle_vt=0
    for t in titres:
        beta=float(t.get("beta",1)); poids=float(t.get("poids",0))/100
        vm=float(t.get("vm",0))
        impact_p=round(beta*var_masi*100,3); impact_m=round(vm*beta*var_masi,2)
        nv=round(vm+impact_m,2); nouvelle_vt+=nv
        resultats.append({"ticker":t.get("ticker",""),"nom":t.get("nom",""),
                           "secteur":t.get("secteur",""),"poids":t.get("poids",0),
                           "beta":beta,"vm_avant":round(vm,2),"impact_p":impact_p,
                           "impact_m":impact_m,"vm_apres":nv})
    resultats.sort(key=lambda x:abs(x["impact_m"]),reverse=True)
    return jsonify({"vt_avant":round(vt,2),"vt_apres":round(nouvelle_vt,2),
                    "variation":round((nouvelle_vt-vt)/vt*100,3) if vt>0 else 0,
                    "impact_mad":round(nouvelle_vt-vt,2),"titres":resultats})

@app.route("/all-tickers")
def all_tickers():
    if not session.get("ok"): return jsonify({"erreur":"Non authentifié"}),401
    return jsonify({"tickers":[{"isin":k,"ticker":v["ticker"],"nom":v["nom"],"secteur":v["secteur"],"prix":v["prix"]} for k,v in ISIN_DB.items()]})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)
