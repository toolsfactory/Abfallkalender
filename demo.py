#!/usr/bin/python3

"""module to read and parse a calendar"""

#"awido.cubefour.de/Customer/zv-muc-so/KalenderICS.aspx?
# oid=00000000-0000-1000-1000-000000000372&jahr=2017&fraktionen=&reminder=-1.17:00"

import sys
import os
import locale
import datetime
from icalendar import Calendar

TYPES = {'rest':'Restmüll wöchentlich', 'gelb':'Gelber Sack', 'bio':'Biotonne', 'sperr':'Sperrmüll'}

def parsecmd():
    """parses the parameters and reads the input file"""
    typ = ''
    txt = ''
    if len(sys.argv) != 3:
        print("Falsche Parameterzahl")
        sys.exit()
    typ = sys.argv[1].lower()
    filename = sys.argv[2]
    if typ in TYPES.keys() or typ == 'next':
        if os.path.exists(filename):
            txt = open(filename, 'r', encoding='utf8').read()
        else:
            print("Fehlende Kalenderdatei")
            sys.exit()
    else:
        print("Falscher Typ")
        sys.exit()
    return typ, txt

def searchnextfortype(typ):
    """find next orccurence of a certain event in the calendar collection"""
    closest = None
    for component in ICAL.walk():
        if component.name == "VEVENT":
            summary = component.get('summary')
            startdt = component.get('dtstart').dt
            #print("Summary: ", summary, " StartDT: ", startdt)
            if summary.startswith(typ) and (startdt >= CT):
                if closest is None:
                    closest = component
                else:
                    if closest.get('dtstart').dt > startdt:
                        closest = component
    return None if closest is None else closest

def findnext():
    """find next occurence over all types supported"""
    nextdt = None
    for key, value in TYPES.items():
        tempdt = searchnextfortype(value)
        if nextdt is None or (tempdt is not None and tempdt.get('dtstart').dt < nextdt.get('dtstart').dt):
            nextdt = tempdt
    return nextdt

def datetostr(caldt):
    """convert a date into 'heute', 'morgen' or day of week"""
    today = datetime.datetime.today().date()
    tomorrow = today + datetime.timedelta(days=1)
    dtdate = caldt
    if dtdate == today:
        return "Heute"
    if dtdate == tomorrow:
        return "Morgen"
    if dtdate > (today + datetime.timedelta(days=6)):
        return caldt.strftime('%d.%m.%Y')
    else:
        return caldt.strftime('%A')


if sys.platform.lower().startswith('linux'):
    locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
else:
    locale.setlocale(locale.LC_ALL, 'deu')

TYP, TXT = parsecmd()
ICAL = Calendar.from_ical(TXT)
CT = datetime.datetime.now().date()
COMP = None

if TYP == 'next':
    COMP = findnext()
else:
    for key, value in TYPES.items():
        if TYP == key:
            COMP = searchnextfortype(value)

if COMP is None:
    print("Fehler")
else:
    #print("{0}".format(COMP.get('dtstart').dt.strftime("%Y-%m-%dT%H:%M:%S")))
    print(datetostr(COMP.get('dtstart').dt))
