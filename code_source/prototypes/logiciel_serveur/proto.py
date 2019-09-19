#Auteur --> aiglematth
#Team   --> HexaCoin

"""
Protocoles du serv
"""

#Imports
from constantes import *
from datetime import datetime as d
from hashlib import sha3_256 as sha3
from pickle import dump, load
from rsa_crypto.crypto import *

#Fonctions
def add_log(infos, mess):
    """
    Ajoute une entrée aux logs
    :param infos: infos du client
    :param mess: le message envoyé
    :return: True ou False
    """
    formatMess = f"""
    ### DEBUT LOG ###
    DATE  --> {str(d.today())}
    IP    --> {infos[0]}
    PORT  --> {infos[1]}
    ERROR --> {mess}
    ### FIN LOG ###"""
    with open(logs, "a") as file:
        if file.write(formatMess) >= 0:
            return True
        else:
            return False

#Classes
class Membre_file():
    """
    Classe qui simplifiera l'utilisation du fichier membres
    """
    def __init__(self):
        """
        Constructeur de la classe
        """
        pass

    def init_file(self, liste):
        """
        Initialise le fichier
        :param liste: liste de tuples (key, ip)
        :return: True si fais, sinon False
        """
        data = {}
        for tupleD in liste:
            data[sha3(tupleD[0].encode()).hexdigest()] = (tupleD[1], tupleD[0])

        try:
            with open(liste_membres, "wb") as file:
                dump(data, file)
                return True
        except:
            return False

    def add_entry(self, liste):
        """
        Rajoute une entrée
        :param liste: liste de tuples (key, ip)
        :return: True si fais, sinon False
        """
        data = {}
        try:
            with open(liste_membres, "rb") as file:
                data = load(file)

            for tupleD in liste:
                data[sha3(tupleD[0].encode()).hexdigest()] = (tupleD[1], tupleD[0])

            with open(liste_membres, "wb") as file:
                dump(data, file)

            return True
        except:
            return False

    def key_is_in(self, key):
        """
        Vérifie si une clef est dans le fichier
        :param key: la clef
        :return: True si oui, sinon False
        """
        data = {}
        with open(liste_membres, "rb") as file:
            data = load(file)

        if key in data:
            return True
        else:
            return False

    def ip_is_in(selfself, ip):
        """
        Vérifie si l'ip est dans le fichier
        :param ip: l'ip
        :return: True si oui, sinon False
        """
        data = {}
        with open(liste_membres, "rb") as file:
            data = load(file)

        for tuple in data.values():
            if ip in tuple[0]:
                return True
        return False

    def key_to(self, hash):
        """
        Permet d'avoir la clef publique d'un user précis
        :param hash: L'username
        :return:     La clef ou False
        """
        data = {}
        with open(liste_membres, "rb") as file:
            data = load(file)

        try:
            return data[hash][1].encode()
        except:
            return False

class Proto_demande():
    """
    Classe du protocole de gestion des demandes...
    Champs :
        - DEMANDE --> qui pourrat être rempli avec ces codes :
        - USERNAME  --> qui sera remplie avec la clef publique hashé

            - 0 --> Demande d'initialisation de mon adresse comme membre --> code de retour :
                - REFERENT : le referent

            - 1 --> Demande d'envoi d'un nouveau référent --> code de retour :
                - REFERENT : le referent

            - 2 --> Suppression de mon adresse de membre --> code de retour :
                - CODE : NIL  --> not in list
                - CODE : GOOD --> fais

            - 3 --> Demande d'envoi des fichiers --> codes retour :
                - SIZE : <taille_du_fichier> --> Reponse valide ;
                    - OK
                - le fichier

            - 4 --> Demande d'inscription  --> code de retour :
                - OK --> je lui signale que je suis à l'écoute de ce qu'il va me proposer
                    - PUBKEY : <publicKey>
                - OK --> si <publicKey> n'est pas dans le fichier, sinon
                - BAD

    """
    def __init__(self, mess, client="", infos=""):
        """
        Constructeur de la classe Proto_init
        :param mess: le message à vérifier...
        :param client: le client
        :param infos: infos client
        """
        #Attributs
        self.mess   = mess
        self.client = client
        self.infos  = infos
        self.init   = "0"
        self.renvoi = "1"
        self.supp   = "2"
        self.file   = "3"
        self.inscr  = "4"
        self.codes  = {self.init   : self.init_client,
                       self.renvoi : self.renvoi_ref,
                       self.supp   : self.supp_client,
                       self.file   : self.send_file,
                       self.inscr  : self.inscription_client}
        self.result_tcheck = self.tcheck()

### METHODES UTILES ###

    def tcheck(self):
        """
        Vérifie le formatage d'une demande
        :return: Le code ou False
        """
        try:
            frag = self.mess.split(",")
            (label_un, label_deux) = (frag[0].split(":"), frag[1].split(":"))
            if label_un[0].strip() == "DEMANDE" and label_un[1].strip() in self.codes:
                return label_un[1].strip()
            elif label_deux[0].strip() == "DEMANDE" and label_deux[1].strip() in self.codes:
                return label_deux[1].strip()
        except:
            pass

        try:
            frag = self.mess.split(":")
            (label, code) = (frag[0].strip(), frag[1].strip())
            if label == "DEMANDE" and code in self.codes:
                return frag[1].strip()
        except:
            return False

### GESTION DE L'INSCRIPTION ###

    def inscription_client(self):
        """
        Implémentation :

        - OK --> je lui signale que je suis à l'écoute de ce qu'il va me proposer
            - PUBKEY : <publicKey>
        - OK --> si <publicKey> n'est pas dans le fichier, sinon
        - BAD

        Inscrit le client
        :return: True si c'est correctement effectué, sinon False
        """
        #Je lui signale que je suis prêt à écouter
        self.client.send(b"OK")
        #Je recois sa demande
        mess = self.client.recv(1024).decode().split(":")
        (champ, clef) = (mess[0].strip(), mess[1].strip())
        #On vérifie la validité de la clef
        if Membre_file().key_is_in(clef) == True or Membre_file().ip_is_in(self.infos[0]) == True:
            print("Client déjà enregistré...Ou ip déjà utilisée...")
            self.client.send(b"BAD")
            return False
        #Sinon on envoi OK apres avoir rajouté le client
        add = Membre_file().add_entry([(clef, self.infos[0])])
        if add == False:
            print("Problème d'ajout...")
            self.client.send(b"BAD")
            return False
        self.client.send(b"OK")
        return True

### GESTION DE L'INIT ###

    def init_client(self):
        """
        Implémentation :

        - RANDOM : <une chaine random>
            - SIGNATURE : <le hash de la chaîne random>
        - OK ou BAD

        Gère l'init
        :return: True ou False
        """
        to_sign = randomString()
        print(f"TOSIGN : {to_sign}")
        #J'envoie la chaîne randomisé
        self.client.send(f"RANDOM : {to_sign}".encode())
        #Reception de la signature
        tupleRecv = self.client.recv(1024).decode().split(",")
        (username, signature) =  (tupleRecv[0].split(":")[1].strip() , tupleRecv[1].split(":")[1].strip())
        #On cherche la clef
        key = Membre_file().key_to(username)
        if key == False:
            print("Key n'est pas dans la liste")
            self.client.send(b"BAD")
            return False
        key = PublicKey(key)
        print(type(signature))
        if key.decrypt(signature).decode() != to_sign:
            self.client.send(b"BAD")
            return False
        do = Membre_file().change_ip_to(username, self.infos[0])
        if do == False:
            self.client.send(b"BAD")
            return False
        self.client.send(b"OK")
        return True

### GESTION DE LA SUPP ###

    def supp_client(self):
        """
        Gère la supp
        :return: True ou False
        """
        pass

### GESTION DU RENVOI DU REFERENT ###

    def renvoi_ref(self):
        """
        Renvoi un ref
        :return: True ou False
        """
        pass

### GESTION DE L'ENVOI FICHIER

    def send_file(self):
        """
        Envoi le fichier
        :return: True ou False
        """
        pass
### ON SATISFAIT LE CLIENT ###

    def satisfait_client(self):
        """
        Satisfait le client ^^
        :return: True ou False
        """
        if self.result_tcheck == False:
            return False
        #Je satisfait le client
        do = self.codes[self.result_tcheck]()
        if do == False:
            return False
        return True

if __name__ == '__main__':
    Membre_file().init_file([("SERVEUR", "192.168.1.1")])
    with open(liste_membres, "rb") as file:
        data = load(file)
        print(data)