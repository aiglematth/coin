#Auteur --> aiglematth
#Team   --> HexaCoin

"""
Fichier qui gère le RSA
"""

#Imports
from Crypto.PublicKey import RSA
from random import randrange, choice
from string import ascii_lowercase

#Fonctions
def generateKey(bits):
    """
    Retourne un objet de type tuple de la forme (clef pub, clef priv)
    :param bits: Nombre de bits sur lequel on code la clef
    :return:     Retourne un objet de type tuple de la forme (clef pub, clef priv)
    """
    key  = RSA.generate(bits)
    pub  = key.exportKey()
    priv = key.publickey().exportKey()
    return (pub, priv)

def randomString():
    """
    Genere une chaine de char aléatoire
    """
    r = ""
    letters = ascii_lowercase
    for i in range(randrange(0,20)):
        r += choice(letters)
    return r

def importKey(key):
    """
    Importe un objet RSA key grâce à une clef (type byte)
    :param key: La clef (en bytes)
    :return:    False ou l'objet RSA key
    """
    try:
        return RSA.importKey(pubKey)
    except:
        return False

#Classes
class PublicKey():
    """
    Classe qui simplifie l'utilisation de la clef publique
    """
    def __init__(self, pubKey):
        """
        Constructeur de la classe PublicKey
        :param pubKey: Une chaîne de bytes qui correspond à une clef publique
        """
        self.publicKey = RSA.importKey(pubKey)

    def decrypt(self, message):
        """
        Decrypte un message
        :param mess: Le mess crypté
        :return: Le mess décrypté ou False
        """
        return self.publicKey.decrypt(message.encode())


class PrivateKey():
    """
    Classe qui simplifie l'utilisation de la clef privée
    """
    def __init__(self, privKey):
        """
        Constructeur de la classe PrivateKey
        :param privKey: Une chaîne de bytes qui correspond à une clef privée
        """
        self.privateKey = RSA.importKey(privKey)

    def encrypt(self, message):
        """
        Encryte le message
        :param message: Le mess en clair
        :return: Le mess crypté ou False
        """
        try:
            return self.privateKey.encrypt(message.encode(), 32)[0].decode()
        except:
            return False


