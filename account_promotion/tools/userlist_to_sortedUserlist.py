import json
import vk_api
import sys

# Можно юзать с консольными аргументами или через перенаправление ввода или ваще руками...

if(len(sys.argv)==3):
    batch_size=int(sys.argv[1])
    param_distr=float(sys.argv[2])
else:
    batch_size=int(input('batch_size:'))
    param_distr=float(input('param_distr:'))

#batch_size = 10
#our_id=179838718
#param_distr=0.0

def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device

vk_session = vk_api.VkApi('+79136387434', '-3.eTvvkqYt-AWK"t>)A`4,_', auth_handler=auth_handler)
vk_session.auth()
vk = vk_session.get_api()

accounts_json=json.loads(open('../output/accounts.txt').read())

#print(accounts_json[0].keys())

reformatted_accs=[(acc['id'],acc['friends']) for acc in accounts_json if ('friends' in acc) and (len(acc['friends'])!=0)]

#print(*reformated_accs)

our_friends = frozenset(vk.friends.get()['items'])
sent_requests = frozenset(vk.friends.getRequests(out=1)['items'])


def commons(p):
    if(p[0] in our_friends or p[0] in sent_requests): return -1;
    return sum((f in our_friends for f in p[1]))

def adds(p):
    if(p[0] in our_friends or p[0] in sent_requests): return -1;
    return sum((p[0] in j[1] for j in reformatted_accs))

def evall(p):
    return param_distr*commons(p)+(1-param_distr)*adds(p) # возможно стоит нормировать оценки

reformatted_accs.sort(key=evall, reverse=True)

#for i,j in reformatted_accs:
#    commons=sum([f in our_friends for f in j])
#    if(commons!=0):
#        print(i,commons)

[print(i,commons((i,j)), adds((i,j)), evall((i,j))) for i,j in reformatted_accs[0:batch_size:] if commons((i,j))>0]
 

