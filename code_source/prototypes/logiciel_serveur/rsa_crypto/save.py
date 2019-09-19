#Auteur --> aiglematth
#Team   --> HexaCoin

"""
Fichier qui gèrera les sauvegardes
"""

#Imports
from pickle import dump, load

#Fonctions
def list_to_dict(objects):
    """
    Transforme une liste de tuples de la forme (user, key) en dict de la forme {user : key}
    :param objects: une liste de tuples (user, key)
    :return: Dict
    """
    new_content = {}
    for tuple in objects:
        new_content[tuple[0]] = tuple[1]
    return new_content

def load_object(path):
    """
    Load un objet
    :param path: le path à load
    :return: False si faux ou l'objet
    """
    try:
        with open(path, "rb") as f:
            return load(f)
    except:
        return False

def dump_new_object(objects, path):
    """
    Dump un objet de plus dans le fichier
    :param object: une liste de tuples (user, key)
    :param path:   le path
    :return:       True si réussi, sinon False
    """
    try:
        #Variables
        new_content = list_to_dict(objects)
        content = load_object(path)
        #On vérifie qu'on peut load le fichier et que le load est un dict
        if content == False or type(content) != dict:
            return False
        for (key, value) in content.items():
            new_content[key] = value
        #On se prépare à dump
        with open(path, "wb") as f:
            dump(new_content, f)
        return True
    except:
        return False

def dump_for_init(objects, path):
    """
    Crée le fichier pour le lancement
    :param objects: Une liste de tuples (user, key)
    :param path:   Le path
    :return:       True si bon, sinon False
    """
    try:
        content = list_to_dict(objects)
        with open(path, "wb") as f:
            dump(content, f)
        return True
    except:
        return False

