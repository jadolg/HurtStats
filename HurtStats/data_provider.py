import json
import re
from string import printable

from untitled2.settings import DATA_FOLDER



def remove_non_ascii_2(text):
    return re.sub(r'[^\x00-\x7F]',' ', text)

def remove_initial_numbers(text):
    return re.sub(r'^[0-9]+', '', text)

def remove_non_printable(text):
    return re.sub("[^{}]+".format(printable), "", text)


def get_data():
    data = open(DATA_FOLDER+'/oxide.covalence.data',"r").read()
    usuarios = json.loads(open(DATA_FOLDER+'/PlayerDatabase.json',"r").read())
    kills = json.loads(open(DATA_FOLDER+'/KillCounter.json',"r").read())
    clans = json.loads(open(DATA_FOLDER+'/ClansData.json',"r").read())
    respuesta = []

    for id in usuarios.get('knownPlayers'):
        mregex = id+"\D\W*(.+)"

        if kills.get(id) != None:
            ukill = kills.get(id)
        else:
            ukill = 0

        nombre = 'Undefined'
        tclan = ''

        try:
            user = json.loads(open(DATA_FOLDER + '/playerdatabase/'+str(id)+'.json', "r").read())
            nombre = user.get('default').get('name')
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
                    break


        if nombre == 'Undefined':
            try:
                nombre = remove_initial_numbers(remove_non_printable(remove_non_ascii_2(re.search(mregex,data).group(1)))).replace("\n","")
            except:
                pass

        usuario = {
            'id' : id,
            'nombre': nombre,
            'clan': tclan,
            'kills': ukill
        }
        respuesta.append(usuario)



    return sorted(respuesta,key=lambda dict: (dict['kills']),reverse=True)
