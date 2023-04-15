
import sqlite3
import random



# Code du jeu
def requete_bd(conn,requete, *params):
   cursor = conn.cursor()
   cursor.execute(requete, params)
   results = cursor.fetchall()
  
   # Validation des changements
   conn.commit()
   return results



# fonction qui génère numméro siret 
def generer_numero_siret():
    siret = ""
    for i in range(14):
        siret += str(random.randint(0, 9))
        i+=1
    return siret



def lancer_jeu(conn):
    rejouer = "oui"
    while rejouer =="oui" :

        print("Bienvenue dans notre jeu de gestion d'entreprise de boulangerie !")
        
        
        # Demander des informations sur l'entreprise et le joueur
        nom = input("quel est ton nom ? ")
        prenom = input("quel est ton prenom ? ")
        pseudo = input("choisi un pseudo : ")
        #Voir si joueur existe dans la table et récupérer toutes ses entreprises
        resultats = requete_bd(conn,"SELECT id FROM Joueur WHERE nom=? AND prenom=? AND pseudo=?;", nom, prenom, pseudo)
        if len(resultats) == 0:
            requete_bd(conn,"INSERT INTO Joueur (nom, prenom, pseudo) VALUES (?, ?, ?);",nom, prenom, pseudo)
            resultats = requete_bd(conn,"SELECT id FROM Joueur WHERE nom=? AND prenom=? AND pseudo=?;", nom, prenom, pseudo)
        id_joueur = resultats[0][0]
        entreprise_joueurs = requete_bd(conn, "SELECT numero_siret FROM Entreprise WHERE id_joueur = ?", id_joueur)
        #afficher entreprise du joueur 
        print("les entreprise trouvées du joueur sont :")
        print(entreprise_joueurs);
        choix = input("Voulez-vous inscrire une nouvelle entreprise : tapez 1 sinon tapez numéro SIRET ")
        if choix == "1": 
            #Demander détails entreprise
    
            numero_siret = generer_numero_siret()
            nom_entreprise = input("Veuillez saisir le nom de votre entreprise : ")
            adresse = input("Veuillez saisir l'adresse de votre entreprise : ")
            requete_bd(conn,"INSERT INTO Entreprise (numero_siret, adresse, nom_entreprise, id_joueur) VALUES (?, ?, ?, ?);",numero_siret, adresse, nom_entreprise, id_joueur)
        else:
            numero_siret = choix
            resultats = requete_bd(conn,"SELECT nom_entreprise FROM Entreprise WHERE numero_siret=? ", numero_siret)

        capital_depart = 5000
        nb_employes = 1
        nb_equipement = 0
        nom_entreprise = nom_entreprise
        print("Bienvenue dans votre entreprise", nom_entreprise)
        print("Votre objectif est de faire prospérer votre entreprise de boulangerie avec un capital de départ de", capital_depart, "$.")
        print("Vous commencez le jeu avec", nb_employes, "employé(s).")
        
        argent_entreprise = capital_depart
        requete_bd(conn,"UPDATE Entreprise SET argent_entreprise=?, nb_employes=?, nb_equipements=? WHERE numero_siret=?",argent_entreprise, nb_employes, nb_equipement, numero_siret)

        
        
        # Premier tour
        print("Tour 1 : ")
        print("Une nouvelle réglementation sur les normes sanitaires a été mise en place par le gouvernement. Si l'entreprise ne se met pas aux normes d'ici la fin du mois, elle risque une amende importante.")
        print("Comment voulez-vous vous mettre aux normes ?")
        print("1. En achetant de nouveaux équipements pour respecter les normes")
        print("2. En embauchant plus de travailleurs pour nettoyer l'entreprise")
        print("3. En faisant des travaux de rénovation pour améliorer l'hygiène")
        choix = input("Saisissez votre choix : ")
        
        if choix == "1":
            print("Vous avez acheté un nouvel appareil de nettoyage nouvelle génération. Le robot était cher, 1000$")
            argent_entreprise -= 1000
        elif choix == "2":
            print("Vous avez embauché un employé supplémentaire. Cela vous coûtera 200$ par tour")
            argent_entreprise -= 200
            nb_employes += 1
        else:
            print("Vous avez effectué des travaux de rénovation pour respecter les normes. Cela vous coûtera 500$")
            argent_entreprise -= 500
        
        print("Votre entreprise dispose de", nb_employes, "employé(s).")
        print("Vous avez", argent_entreprise, "$ d'argent restant.")
        #sauvegarder dans la base de données
        requete_bd(conn,"UPDATE Entreprise SET argent_entreprise=?, nb_employes=?, nb_equipements=? WHERE numero_siret=?",argent_entreprise, nb_employes, nb_equipement, numero_siret)
        
        # Deuxième tour
        print("Tour 2 : ")
        print("Le four principal est tombé en panne. Que voulez-vous faire ?")
        print("1. Réparer le four")
        print("2. Acheter un nouveau four")
        print("3. Louer un four temporaire")
        choix = input("Saisissez votre choix : ")
        
        if choix == "1":
            print("Bravo bricolo, Vous avez réparé le four principal. Néanmoins, il fallait acheter les pièces de rechange. cela vous a couté 200$.")
            argent_entreprise -= 200
        elif choix == "2":
            print("Félicitation, Vous avez acheté un nouveau four supertop pour votre boulangerie. Encore une dépense : 500$.")
            argent_entreprise -= 500
        else:
            print("mouais, Vous avez loué un four temporaire, vous êtes un peu radin. 100$ la loc.")
            argent_entreprise -= 100
            nb_equipement += 1
            print("Le four est beaucoup plus petit que l'ancien, la production de pain sera donc réduite.")
            
            print("Vous disposez maintenant de ", argent_entreprise, "$ d'argent restant.")
        #sauvegarder dans la base de donnee
        requete_bd(conn,"UPDATE Entreprise SET argent_entreprise=?, nb_employes=?, nb_equipements=? WHERE numero_siret=?",argent_entreprise, nb_employes, nb_equipement, numero_siret)
            
            
        # Début du troisième tour
        
        
        # Annonce de la proposition présidentielle
        print("Le président de la République a besoin de baguettes pour accueillir Joe Biden. C'est un événement spécial.")
        print("Que souhaitez-vous faire ?")
        print("1. Accepter la proposition et produire des baguettes pour l'événement.")
        print("2. Refuser la proposition et continuer la production normale de baguettes.")
        
        # Demande de choix au joueur
        choix = input("Entrez votre choix (1 ou 2) : ")
        
        # Si le joueur accepte la proposition
        if choix == "1":
          print("Vous avez choisi d'accepter la proposition présidentielle.")
        
          # Vérification du nombre d'employés disponibles
          if nb_employes == 2:
            # Production de baguettes en grande quantité
            print("Vous avez suffisamment d'employés pour produire un grand nombre de baguettes.")
            argent_entreprise += 650
            print("Vous gagnez 650$ d'argent pour votre entreprise.")
          elif nb_equipement == 1:
            # Production de baguettes réduite à cause du four temporaire
            print("Malheureusement, la production de baguettes est réduite en raison de la location du four temporaire.")
            argent_entreprise += 300
            print("Vous gagnez 300$ d'argent pour votre entreprise.")
          elif nb_employes == 1:
              # Production de baguettes de qualité supérieure
              print("Vous n'avez qu'un seul employé, mais vous pouvez produire des baguettes de meilleure qualité.")
              argent_entreprise += 600
              print("Vous gagnez 600$ d'argent pour votre entreprise.")
        
        # Si le joueur refuse la proposition
        elif choix == "2":
          print("Vous avez choisi de refuser la proposition présidentielle.")
          print("La production de baguettes continue normalement.")
        else:
          print("Choix invalide.")
          
          
        # Fin du troisième tour
        print("Fin du troisième tour :")
        print("Le score actuel de l'entreprise est de",argent_entreprise)
          
        #sauvegarder dans la base de donnee
        requete_bd(conn,"UPDATE Entreprise SET argent_entreprise=?, nb_employes=?, nb_equipements=? WHERE numero_siret=?",argent_entreprise, nb_employes, nb_equipement, numero_siret)
        requete_bd(conn,"INSERT INTO Score (nom_joueur, score, numero_siret,id_joueur) VALUES (?, ?, ?, ?);",nom, argent_entreprise, numero_siret,id_joueur)
        if argent_entreprise < 4500:
            print("L'interface annonce que l'entreprise a été mal gérée.")
        else:
            print("L'interface annonce que l'entreprise a été bien gérée.")
        
        rejouer = input("Souhaitez-vous rejouer ? (oui/non) ")
        if rejouer.lower() == "oui":
            # Le joueur souhaite rejouer, on recommence le jeu du début
            print("Le jeu recommence du début.")
            
        else:
            # Le joueur ne souhaite pas rejouer, on affiche un message de fin
            print("Fin du jeu, merci et à bientôt.")
            
def creation_table(conn, req_create_table):
    cursor = conn.cursor()
    cursor.execute(req_create_table)
    conn.commit()
      
# Connexion à la base de données
conn = sqlite3.connect('Ines&Noe.db')

# Création de la table entreprise
requete_entreprise = '''CREATE TABLE if not exists Entreprise
                (numero_siret INTEGER PRIMARY KEY,
                 adresse TEXT NOT NULL,
                 nom_entreprise TEXT NOT NULL,
                 argent_entreprise REAL,
                 nb_employes INTEGER,
                 nb_equipements REAL,
                 id_joueur INTEGER,
                 FOREIGN KEY (id_joueur) REFERENCES Joueur(id));'''
creation_table(conn,requete_entreprise)


# Création de la table Joueur
requete_joueur='''CREATE TABLE if not exists Joueur
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nom TEXT NOT NULL,
                 prenom TEXT NOT NULL,
                 pseudo TEXT NOT NULL);'''
creation_table(conn,requete_joueur)

                
# Création de la table Scores
requete_score = '''CREATE TABLE if not exists Score
                (id INTEGER PRIMARY KEY,
                 nom_joueur TEXT,
                 score INTEGER,
                 numero_siret INTEGER,
                 id_joueur INTEGER,
                 FOREIGN KEY (numero_siret) REFERENCES Entreprise(numero_siret),
                 FOREIGN KEY (id_joueur) REFERENCES Joueur(id));'''

creation_table(conn,requete_score)      
lancer_jeu(conn)   

#fermer conn
conn.close()