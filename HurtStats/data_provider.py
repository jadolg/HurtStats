import json
import re
from string import printable

from untitled2.settings import DATA_FOLDER, BANLIST


def remove_non_ascii_2(text):
    return re.sub(r'[^\x00-\x7F]',' ', text)

def remove_initial_numbers(text):
    return re.sub(r'^[0-9]+', '', text)

def remove_non_printable(text):
    return re.sub("[^{}]+".format(printable), "", text)


def get_data():
    # data = open(DATA_FOLDER+'/oxide.covalence.data',"r").read()
    usuarios = json.loads(open(DATA_FOLDER+'/PlayerDatabase.json',"r").read())
    kills = json.loads(open(DATA_FOLDER+'/KillCounter.json',"r").read())
    clans = json.loads(open(DATA_FOLDER+'/ClansData.json',"r").read())
    banks = json.loads(open(DATA_FOLDER+'/Banks.json',"r").read())
    banned_list = []
    ips = []
    dups = []

    for ban_id in open(BANLIST, 'r').readlines():
        banned_list.append(ban_id.strip('\n').strip('\r'))

    respuesta = []

    for id in usuarios.get('knownPlayers'):
        banned = str(id) in banned_list

        if banned:
            continue

        mregex = id+"\D\W*(.+)"

        if kills.get(id) != None:
            ukill = kills.get(id)
        else:
            ukill = 0

        nombre = 'Undefined'
        tclan = ''
        dirty = False



        try:
            user = json.loads(open(DATA_FOLDER + '/playerdatabase/'+str(id)+'.json', "r").read())
            nombre = user.get('name').strip('"')
            ip = user.get('ip').strip('"')

            if not ip in ips:
                ips.append(ip)
            else:
                dups.append(ip)

            steamid = user.get('steamid').strip('"')

            if not str(steamid).startswith(ip.replace('.','')):
                dirty = True
        except:
            pass

        for clan in clans:
            if tclan != '':
                break
            for member in clan.get('members'):
                if member.get('id').get('m_SteamID') == int(id):
                    tclan = clan.get('clanTag')
                    if nombre == 'Undefined':
                        nombre = member.get('name')
                        dirty = True
                    break


        # if nombre == 'Undefined':
        #     try:
        #         nombre = remove_initial_numbers(remove_non_printable(remove_non_ascii_2(re.search(mregex,data).group(1)))).replace("\n","")
        #     except:
        #         pass

        money = 0

        try:
            money = float(banks.get('List_accounts').get(id).get('current')) + float(banks.get('List_accounts').get(id).get('poket'))
        except:
            pass

        usuario = {
            'id' : id,
            'ip' : ip,
            'nombre': nombre,
            'clan': tclan,
            'kills': ukill,
            'money': money,
            'dirty': dirty,
            'banned':banned,
            'duplicated_ip' : 0
        }
        respuesta.append(usuario)

    for i in respuesta:
        if i['ip'] in dups:
            i['duplicated_ip'] = True

    return sorted(respuesta,key=lambda dict: (dict['kills'],dict['money']),reverse=True)


def get_clans(data):
    result = []
    clans = json.loads(open(DATA_FOLDER + '/ClansData.json', "r").read())
    for clan in clans:
        kills = 0
        member_sum = len(clan.get('members'))
        for member in clan.get('members'):
            for m in data:
                if int(m['id']) == member.get('id').get('m_SteamID'):
                    kills += m['kills']
                    break

        theclan = {
            'nombre' : clan.get('clanTag'),
            'miembros' : member_sum,
            'color' : clan.get('clanTagColor'),
            'kills' : kills
        }

        result.append(theclan)

    return sorted(result, key=lambda dict: (dict['kills']), reverse=True)


