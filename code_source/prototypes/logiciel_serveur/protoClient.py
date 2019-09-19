#Auteur --> aiglematth
#Team   --> HexaCoin

"""
Protocoles du client
"""

#Imports
from hashlib import sha3_256 as sha3
from rsa_crypto.crypto import *

#Classes
class Proto_response():
    """
    Classe du protocole de réponse
    """
    def __init__(self, serveur, key):
        """
        Constructeur de la classe
        :param serveur: Serveur
        :param key: Ma clef
        """
        self.serv = serveur
        self.key = key
        self.init   = "0"
        self.renvoi = "1"
        self.supp   = "2"
        self.file   = "3"
        self.inscr  = "4"
        self.codes  = {self.init   : self.init_me,
                       self.renvoi : self.renvoi_ref,
                       self.supp   : self.supp_me,
                       self.file   : self.recv_file,
                       self.inscr  : self.inscrption}

### METHODES UTILES ###

    def formatDemande(self, code):
        """
        Formate une demande
        :param code:
        :return:
        """
        if code != self.inscr:
            return f"DEMANDE : {code},{self.formatPubKey()}"
        else:
            return f"DEMANDE : {code}"

    def formatPubKey(self):
        """
        Formate une demande
        :return: La chaine formatée
        """
        return f"USERNAME : {self.key.exportKey().decode()}"

    def formatUsername(self):
        """
        Formate l'username
        :return: La chaîne formatée
        """
        return f"USERNAME : {sha3(self.key.exportKey()).hexdigest()}"

    def formatSignature(self, to_sign):
        """
        Format la signature
        :param to_sign: La string à signer
        :return: La signature fomtée
        """
        format = self.key.publickey().encrypt(to_sign.encode(), 32)[0].hex()
        print(format)
        return f"SIGNATURE : {format}"

### GESTION DE L'INSCRIPTION ###

    def inscrption(self):
        """
        M'inscrit
        :return: True si c'est correctement fais, sinon False
        """
        #On envoi la demande
        mess = self.formatDemande(self.inscr)
        print(f"C > {mess}")
        self.serv.send(mess.encode())
        #On attend la réponse
        rep = self.serv.recv(1024).decode()
        print(f"S > {rep}")
        if rep != "OK":
            return False
        #J'envoi une demande PUBKEY : <maKey>
        mess = self.formatPubKey()
        print(f"C > {mess}")
        self.serv.send(mess.encode())
        #J'attends la réponse
        rep = self.serv.recv(1024).decode()
        print(f"S > {rep}")
        if rep != "OK":
            return False
        return True

### GESTION DE L'INIT ###

    def init_me(self):
        """
        Gère l'init
        :return: True ou False
        """
        demande = self.formatDemande("0")
        self.serv.send(demande.encode())
        #On attend sa rep
        rep = self.serv.recv(1024).decode().split(":")
        print(rep)
        (champ, string) = (rep[0].strip(), rep[1].strip())
        if champ != "RANDOM":
            return False

        demande = self.formatUsername() + "," + self.formatSignature(string)
        self.serv.send(demande.encode())
        #On attend la rep
        rep = self.serv.recv(1024).decode()
        print(rep)
        if rep == "BAD":
            return False
        return True

### GESTION DE LA SUPP ###

    def supp_me(self):
        """
        Gère la supp
        :return: True ou False
        """
        pass

### GESTION DU RENVOI DU REFERENT ###

    def renvoi_ref(self):
        """
        Recoit un ref
        :return: True ou False
        """
        pass

### GESTION DE L'ENVOI FICHIER

    def recv_file(self):
        """
        Envoi le fichier
        :return: True ou False
        """
        pass


if __name__ == '__main__':
    from Crypto.PublicKey import RSA
    from socket import socket, AF_INET, SOCK_STREAM
    from sys import argv
    key = RSA.generate(1024)
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect(("192.168.1.17", int(argv[1])))
        p = Proto_response(s, key)
        p.inscrption()
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect(("192.168.1.17", int(argv[1])))
        p = Proto_response(s, key)
        p.init_me()
