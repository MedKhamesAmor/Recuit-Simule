import random
import math


def calculer_distance_totale(solution, matrice_distances):
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale


def generer_voisin(solution):
    """Génère un voisin en échangeant deux villes aléatoires"""
    voisin = solution.copy()
    i, j = random.sample(range(len(solution)), 2)
    voisin[i], voisin[j] = voisin[j], voisin[i]
    return voisin


def recuit_simule(matrice_distances, temperature_initiale, temperature_finale, taux_refroidissement,
                  iterations_par_temperature):
    nombre_villes = len(matrice_distances)

    # Solution initiale aléatoire
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)

    distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)

    meilleure_solution = solution_actuelle.copy()
    meilleure_distance = distance_actuelle

    temperature = temperature_initiale

    while temperature > temperature_finale:
        for _ in range(iterations_par_temperature):
            # Générer un voisin
            solution_voisine = generer_voisin(solution_actuelle)
            distance_voisine = calculer_distance_totale(solution_voisine, matrice_distances)

            # Calculer la différence de distance
            delta_distance = distance_voisine - distance_actuelle

            # Accepter la solution si elle est meilleure ou avec une probabilité selon la température
            if delta_distance < 0 or random.random() < math.exp(-delta_distance / temperature):
                solution_actuelle = solution_voisine
                distance_actuelle = distance_voisine

                # Mettre à jour la meilleure solution
                if distance_voisine < meilleure_distance:
                    meilleure_solution = solution_voisine.copy()
                    meilleure_distance = distance_voisine

        # Refroidissement
        temperature *= taux_refroidissement

    return meilleure_solution, meilleure_distance


# Matrice des distances
matrice_distances = [
    [0, 2, 2, 7, 15, 2, 5, 7, 6, 5],
    [2, 0, 10, 4, 7, 3, 7, 15, 8, 2],
    [2, 10, 0, 1, 4, 3, 3, 4, 2, 3],
    [7, 4, 1, 0, 2, 15, 7, 7, 5, 4],
    [7, 10, 4, 2, 0, 7, 3, 2, 2, 7],
    [2, 3, 3, 7, 7, 0, 1, 7, 2, 10],
    [5, 7, 3, 7, 3, 1, 0, 2, 1, 3],
    [7, 7, 4, 7, 2, 7, 2, 0, 1, 10],
    [6, 8, 2, 5, 2, 2, 1, 1, 0, 15],
    [5, 2, 3, 4, 7, 10, 3, 10, 15, 0]
]

# Paramètres du Recuit Simulé
temperature_initiale = 1000
temperature_finale = 0.1
taux_refroidissement = 0.95
iterations_par_temperature = 100

# Exécution de l'algorithme
meilleure_solution, meilleure_distance = recuit_simule(
    matrice_distances,
    temperature_initiale,
    temperature_finale,
    taux_refroidissement,
    iterations_par_temperature
)

# Affichage des résultats
print("Meilleure solution trouvée (Recuit Simulé):", meilleure_solution)
print("Distance minimale:", meilleure_distance)

# Affichage du parcours optimal formaté
parcours_formate = ["V" + str(ville + 1) for ville in meilleure_solution]
print("\nParcours optimal:", parcours_formate)