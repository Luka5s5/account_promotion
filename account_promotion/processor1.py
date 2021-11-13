import json
import openpyxl
from pathlib import Path
from account_promotion.utils import *
import matplotlib.pyplot as plt

with open("output/accounts.txt","r") as f:
    users = json.load(f)
oname = "output.xlsx"

try:
    with open("output/cutted.txt","r") as f:
        users = json.load(f)
except Exception:
    final_ids = []
    for user in users:
        final_ids += [user["id"]]

    i = 0
    for user in users:
        if (i % 100 == 0):
            print(i)
        i += 1
        lst = []
        if (not "friends" in user):
            break 
        for id2 in user["friends"]:
            if (id2 in final_ids):
                lst += [id2]
        user["friends"] = lst
        
    save_as_json(users, "output/cutted.txt")

active = dict()
for i in range(0,1000):
    active[i] = 0
for user in users:
    if (not "friends" in user):
        break
    if (len(user["friends"]) in active):
        active[len(user["friends"])] += 1

for i in range(999, 0, -1):
    active[i - 1] += active[i]

keys = list(active.keys())[:50]
values = list(active.values())[:50]
plt.bar(keys, values)
plt.ylabel("Number of people")
plt.xlabel("len(friends)")
plt.show()
 
# wb.save(oname)
