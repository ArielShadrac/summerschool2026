"""
╔══════════════════════════════════════════════════════════════════════╗
║  CITADEL · Summer School 2025 · TP Déploiement — Phase 1           ║
║  Fichier : 03_test.py                                               ║
║  Objectif : Valider que l'API déployée fonctionne correctement      ║
╚══════════════════════════════════════════════════════════════════════╝

Contexte
--------
Votre API tourne sur http://localhost:8000.
Ce script envoie des requêtes HTTP et vérifie les réponses.
C'est ce qu'on appelle des tests d'intégration.

Instructions
------------
Complétez les TODO dans l'ordre.
Prérequis : 01_train.py ET 02_serve.py exécutés avec succès.

Usage:
    python 03_test.py
"""

import requests

API_BASE = "http://localhost:8000"

# ── Couleurs terminal ─────────────────────────────────────────────────────────
VERT   = "\033[92m"
ROUGE  = "\033[91m"
JAUNE  = "\033[93m"
RESET  = "\033[0m"
GRAS   = "\033[1m"


# ══════════════════════════════════════════════════════════════════════════════
# ÉTAPE 1 — Vérifier que l'API est accessible
# ══════════════════════════════════════════════════════════════════════════════

def tester_health():
    """
    Envoyer une requête GET sur /health et vérifier la réponse.

    La réponse doit contenir :
        - "status" == "ok"
        - "modele" non vide
        - "accuracy" > 0

    Retourne True si l'API est en bonne santé, False sinon.
    """
    print(f"\n{GRAS}[TEST 1] Health check{RESET}")

    try:
        # TODO 1a — Envoyer une requête GET sur /health
        # Indice : requests.get(f"{API_BASE}/health", timeout=5)
        reponse = ...  # TODO

        # TODO 1b — Vérifier que le code HTTP est 200
        # Indice : reponse.status_code
        if ...:  # TODO : condition pour code != 200
            print(f"  {ROUGE}✗ Code HTTP inattendu : {reponse.status_code}{RESET}")
            return False

        # TODO 1c — Décoder le JSON de la réponse
        data = ...  # TODO : reponse.json()

        # TODO 1d — Vérifier que "status" == "ok"
        if ...:  # TODO
            print(f"  {ROUGE}✗ Status inattendu : {data}{RESET}")
            return False

        print(f"  {VERT}✓ API accessible{RESET}")
        print(f"  Modèle  : {data.get('modele')}")
        print(f"  Accuracy: {data.get('accuracy', 0):.1%}")
        return True

    except requests.exceptions.ConnectionError:
        print(f"  {ROUGE}✗ Impossible de joindre l'API sur {API_BASE}{RESET}")
        print(f"  → Vérifiez que 02_serve.py tourne : uvicorn 02_serve:app --port 8000")
        return False


# ══════════════════════════════════════════════════════════════════════════════
# ÉTAPE 2 — Tester une prédiction
# ══════════════════════════════════════════════════════════════════════════════

def tester_prediction(texte: str, label_attendu: str, description: str) -> bool:
    """
    Envoyer un texte à /predict et vérifier que le label retourné est correct.

    Paramètres :
        texte          : le texte à analyser
        label_attendu  : "positif" ou "négatif"
        description    : description du test pour l'affichage

    Retourne True si la prédiction est correcte.
    """
    try:
        # TODO 2a — Envoyer une requête POST sur /predict
        # Le corps doit être : {"texte": texte}
        # Indice : requests.post(url, json={"texte": texte}, timeout=10)
        reponse = ...  # TODO

        # TODO 2b — Décoder la réponse JSON
        data = ...  # TODO

        # TODO 2c — Extraire le label prédit
        label_predit = ...  # TODO : data["label"]
        score        = ...  # TODO : data["score"]

        # TODO 2d — Comparer avec le label attendu
        succes = label_predit == label_attendu

        # Affichage du résultat
        icone  = f"{VERT}✓{RESET}" if succes else f"{ROUGE}✗{RESET}"
        statut = f"{VERT}OK{RESET}"  if succes else f"{ROUGE}ÉCHEC{RESET}"
        print(f"  {icone} [{statut}] {description}")
        print(f"      Texte   : \"{texte[:60]}\"")
        print(f"      Attendu : {label_attendu}  |  Prédit : {label_predit}  |  Score : {score:.1%}")

        return succes

    except Exception as e:
        print(f"  {ROUGE}✗ Erreur : {e}{RESET}")
        return False


# ══════════════════════════════════════════════════════════════════════════════
# ÉTAPE 3 — Tester les cas limites
# ══════════════════════════════════════════════════════════════════════════════

def tester_texte_vide() -> bool:
    """
    Vérifier que l'API retourne une erreur 400 pour un texte vide.

    Un bon service API doit rejeter les entrées invalides avec
    un code d'erreur explicite, pas crasher ou retourner n'importe quoi.
    """
    print(f"\n{GRAS}[TEST 3] Texte vide → erreur 400 attendue{RESET}")

    # TODO 3 — Envoyer une requête avec texte vide et vérifier le code 400
    # Indice : {"texte": ""}
    # Indice : reponse.status_code == 400
    reponse = ...  # TODO

    if ...:  # TODO : condition pour code == 400
        print(f"  {VERT}✓ Erreur 400 retournée correctement{RESET}")
        return True
    else:
        print(f"  {ROUGE}✗ Code attendu: 400, reçu: {reponse.status_code}{RESET}")
        return False


# ══════════════════════════════════════════════════════════════════════════════
# SUITE DE TESTS — Ne pas modifier
# ══════════════════════════════════════════════════════════════════════════════

CAS_DE_TEST = [
    # (texte, label_attendu, description)
    ("Ce service est excellent, je suis très satisfait !", "positif", "Avis clairement positif"),
    ("Arnaque totale, je déconseille fortement.",           "négatif", "Avis clairement négatif"),
    ("Livraison rapide, produit conforme.",                 "positif", "Avis positif court"),
    ("Mauvaise qualité, tombé en panne rapidement.",        "négatif", "Avis négatif factuel"),
    ("Parfait, exactement ce que je cherchais !",           "positif", "Avis enthousiaste"),
    ("Très déçu, je ne recommande pas du tout.",            "négatif", "Avis déçu explicite"),
]

if __name__ == "__main__":
    print("=" * 60)
    print("  CITADEL · Tests d'intégration — Sentiment API")
    print("=" * 60)

    # Test 1 : health check
    if not tester_health():
        print(f"\n{ROUGE}API inaccessible — arrêt des tests.{RESET}")
        exit(1)

    # Test 2 : prédictions
    print(f"\n{GRAS}[TEST 2] Prédictions sur {len(CAS_DE_TEST)} cas{RESET}")
    resultats = []
    for texte, label_attendu, description in CAS_DE_TEST:
        ok = tester_prediction(texte, label_attendu, description)
        resultats.append(ok)
        print()

    # Test 3 : cas limite
    ok_limite = tester_texte_vide()

    # Récapitulatif
    n_ok    = sum(resultats) + ok_limite
    n_total = len(resultats) + 1
    print("\n" + "=" * 60)
    print(f"  Résultat : {n_ok}/{n_total} tests réussis")
    if n_ok == n_total:
        print(f"  {VERT}{GRAS}✅  Tous les tests passent — API prête pour la démo !{RESET}")
    else:
        print(f"  {JAUNE}⚠️   Quelques tests échouent — vérifiez votre implémentation.{RESET}")
    print("=" * 60)
