import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproj.settings")
 
import csv
from apartment.models import Heya
 
reader = csv.reader(open("kaijyu-1.csv"))
 
for r in reader:
    print r
    h = Heya()
    h.tanako = r[0].decode('cp932').encode('utf-8')
    h.bango = r[1]
    h.hirosa = r[2]
    h.yachin = r[3]
    h.save()