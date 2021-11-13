import json
from threading import *
import vk_api
import time
import copy
from pathlib import Path
from account_promotion.utils import *
from account_promotion.vk import *

def append_group_members(response, array):
    if (len(response["items"]) == 0):
        return False
    for member in response["items"]:
        array.append(member)
    return True

def append_friends(response, account):
    account["friends"] = []
    for friend in response["items"]:
        account["friends"].append(friend)

vk = vk_collection(sleep=0.4)
with open(vkconfig_iname) as f:
    config = json.load(f)
SAVING_EVERY = 100


# Downloading from groups
try:
    with open(groups_oname) as f:
        groups = json.load(f)
except Exception:
    groups = []

for i in range(len(config["groups"])): 
    g_id = config["groups"][i]
    print("downloading group " + str(g_id))
    if (g_id in [group["id"] for group in groups]):
        continue
    j = 0
    users = [] 
    while(True):
        print("Status " + str(j * 1000))
        OK = vk.direct_call("groups.getMembers",
                        {"group_id": g_id,
                        "offset": j*1000,
                        "count": 1000,
                        "fields": config["fields"]},
                    append_group_members,
                    array=users
        )
        if (not OK):
            break
        j += 1
    groups.append({"id": g_id, "members": users})  
    save_as_json(groups, groups_oname)

# Creating or downloading accounts
try:
    with open(accounts_oname) as f:
        accounts = json.load(f)
    ids = [account["id"] for account in accounts]
except Exception:
    accounts = []
    ids = []
    for group in groups:
        for user in group["members"]:
            if (user["id"] in ids) or ("deactivated" in user and user["deactivated"] == "banned") or ("deactivated" in user and user["deactivated"] == "deleted") or ("can_access_closed" in user and user["can_access_closed"] == False) or (user["has_photo"] == 0) or (user["can_write_private_message"] == 0) or ("last_seen" not in user) or (time.time() - user["last_seen"]["time"] > 14*24*60*60):
                continue
            accounts += [user]
            ids += [user["id"]]
    save_as_json(accounts, accounts_oname)

# Downloading friends
print("Accounts size: " + str(len(accounts)))
for i in range(len(accounts)):
    print("downloading friends: " + str(i))
    account = accounts[i] 
    if ("friends" in account): # for savings
        continue
    # add_task or direct_call
    vk.add_task("friends.get",
                {"user_id": account["id"]},
            append_friends,
            account=account
    ) 
    if (i % SAVING_EVERY == SAVING_EVERY - 1):
        save_as_json(accounts, accounts_oname)
vk.execute_tasks()
save_as_json(accounts, accounts_oname)

print("Ok, now you have a graph")
