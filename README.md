# coin

Ce projet n'aboutira jamais, il fait echo à un projet mené par quelqu'un d'autre, et j'ai simplement commencé à implémenter
une partie de son projet. Malgré tout ce code a été fais a 100% par moi, je ne permettrais pas de voler du code non fais par ma persone.

Mes codes sont l'implémentation d'un serveur permettant de s'authentifier afin d'entrer dans le réseau Peer To Peer de ce projet.
Le logiciel client est aussi présent et fonctionnel

### Implémentations ###

  --> Système d'authentification sécurisé (avec chiffrement asymétrique)
  
  --> Système de paquets sécurisés par un principe de jeu de mots ( on envoi un mot que la personne doit crypter dans son prochain
      paquet, si le mot une fois décrypté est bien le bon, on sait que le paquet provient bien de la personne voulue ) qui permet 
      d'assurer l'authenticité du paquet
  
  --> Plusieurs ébauches de protocoles maison, d'authentification, de gestion des erreurs et autres (je vous laisse découvrir le 
      code si vous êtes intéréssés)
  
### Ce que j'ai appris ###

  --> L'implémentation d'un protocole n'est pas une chose facile !! Elle mérite une préparation théorique papier importante avant
      de se lancer dans la partie code...j'en ai fais les frais car le premier protocole que j'ai fourni était spoofable...et le 
      second assure l'authenticité, un système d'adressage fiable, mais n'assure pas l'intégrité du message ni sa confidentialité !
      
  --> J'adore le réseau, avant cela, j'aimais bien le réseau, mais pas plus, maintenant je suis fou de lui !! C'est magique
      comment tout est si bien orchestré !!
      
Comme d'habitude, récupérez, améliorez et adaptez ce code autant que vous le voulez.

Si vous souhaitez me contacter, mon mail : aiglematth@pprotonmail.com
