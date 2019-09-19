#Auteur --> aiglematth
#Team   --> HexaCoin

"""
Ce fichier contiendra tout les outils de gestion du réseau (socket)
"""

#Imports
from socket import socket, AF_INET, SOCK_STREAM
from constantes import *
from proto import *
#--> Possible ajout de la gestion de logs d'erreurs

#Fonctions


#Classes
class Server():
    """
    Classe qui gèrera le serveur
    """
    def __init__(self, port):
        """
        Constructeur de la classe
        :param port: int port
        """
        #Attributs
        self.port = port
        self.host = ""
        #Méthodes
        self.runServ()

    def runServ(self):
        """
        Lance le serveur
        :return: None
        """
        with socket(AF_INET, SOCK_STREAM) as s:
            print("### SERVEUR LANCE ###")
            #Attente
            s.bind(("", self.port))
            #Nbr d'écoutes
            s.listen(5)
            #Boucle infinie
            while True:
                #Accept d'un client
                (client, infos) = s.accept()
                print("### CLIENT ###")
                print(f"IP   --> {infos[0]}")
                print(f"PORT --> {infos[1]}")
                #Reception du message
                mess = client.recv(1024).decode().upper()
                if Proto_demande(mess).result_tcheck != False:
                    #Code à effectuer s'il y a une demande d'initialisation
                    Proto_demande(mess, client, infos).satisfait_client()
                elif mess == verification:
                    #Code à effectuer s'il y a une demande de vérification
                    pass
                else:
                    #Code à effectuer si aucun cas n'est correspondant
                    #self.add_log(infos, "ERREUR DE FORMATAGE")
                    Proto_error(client).format_error()

                print("### FIN CLIENT ###")


