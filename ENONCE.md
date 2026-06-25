# TP DÉPLOIEMENT — Phase 1
## CITADEL · Summer School 2025

---

## Contexte

Un opérateur mobile en Afrique de l'Ouest reçoit chaque jour des milliers
d'avis clients sur son application. Il est impossible de les lire manuellement.

**Votre mission :** construire et déployer un système capable d'analyser
automatiquement le sentiment de chaque avis (POSITIF ou NÉGATIF) et de le
rendre accessible via une API REST et une interface web.

---

## Ce que vous devez produire

À la fin du TP, votre groupe doit avoir :

| # | Livrable | Validation |
|---|---|---|
| 1 | `01_train.py` complété et fonctionnel | `python 01_train.py` → 3 fichiers dans `model/sentiment/` |
| 2 | `02_serve.py` complété et fonctionnel | `uvicorn 02_serve:app --port 8000` → API répond |
| 3 | `03_test.py` complété | `python 03_test.py` → tous les tests passent |
| 4 | (bonus) Interface web dans `app/index.html` | `http://localhost:8000/app` affiche une UI |

---

## Structure des fichiers

```
phase1_sentiment/
├── 01_train.py      ← Compléter les TODO (entraînement + sérialisation)
├── 02_serve.py      ← Compléter les TODO (API FastAPI)
├── 03_test.py       ← Compléter les TODO (tests d'intégration)
├── model/           ← Créé automatiquement par 01_train.py
│   └── sentiment/
│       ├── vectorizer.pkl
│       ├── classifier.pkl
│       └── meta.json
└── app/
    └── index.html   ← Bonus : interface web
```

---

## Ordre d'exécution

```
1. python 01_train.py
         ↓
   model/sentiment/ créé avec 3 fichiers

2. uvicorn 02_serve:app --host 0.0.0.0 --port 8000 --reload
         ↓
   API accessible sur http://localhost:8000

3. python 03_test.py   (dans un second terminal)
         ↓
   7/7 tests réussis

4. (Bonus) Créer app/index.html
         ↓
   http://localhost:8000/app affiche l'interface
```

---

## Indices par niveau

### Niveau 1 — En cas de blocage total sur un TODO

Lisez attentivement les commentaires au-dessus de chaque TODO.
Ils contiennent les noms des fonctions et classes à utiliser.

### Niveau 2 — Si le niveau 1 ne suffit pas

**TODO 1 (preparer_donnees) :**
```python
textes = [t for t, _ in dataset]
labels = [l for _, l in dataset]
```

**TODO 2 (creer_vectoriseur) :**
```python
return TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
```

**TODO 3 (entrainer) :**
```python
X_train     = vectoriseur.fit_transform(textes_train)
classifieur = LogisticRegression(max_iter=1000)
classifieur.fit(X_train, labels_train)
```

**TODO 4 (evaluer) :**
```python
X_test      = vectoriseur.transform(textes_test)   # transform, pas fit_transform !
predictions = classifieur.predict(X_test)
print(classification_report(labels_test, predictions, target_names=["négatif","positif"]))
accuracy    = accuracy_score(labels_test, predictions)
```

**TODO 5 (sauvegarder) :**
```python
with open(MODEL_DIR / "vectorizer.pkl", "wb") as f:
    pickle.dump(vectoriseur, f)
with open(MODEL_DIR / "classifier.pkl", "wb") as f:
    pickle.dump(classifieur, f)
meta = {"type":"tfidf+logreg", "classes":["négatif","positif"], "accuracy": accuracy}
(MODEL_DIR / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
```

### Niveau 3 — Solution complète

Disponible auprès du formateur si votre groupe est bloqué depuis plus de 20 min
après avoir essayé les niveaux 1 et 2.

---

## Questions de réflexion (à discuter en groupe)

1. **Sérialisation :** Pourquoi utilise-t-on `pickle` pour sauvegarder le modèle ?
   Quelles sont ses limites ?

2. **transform vs fit_transform :** Pourquoi utilise-t-on `.transform()` sur les données
   de test et `.fit_transform()` sur les données d'entraînement ?

3. **Lifespan FastAPI :** Pourquoi charge-t-on le modèle dans `lifespan` et non
   dans la fonction `predire_sentiment` directement ?

4. **Latence :** Que se passerait-il si on chargeait le modèle à chaque requête ?
   Comment le mesureriez-vous ?

5. **Limites :** Testez avec un texte en mooré ou en anglais. Que se passe-t-il ?
   Pourquoi ?

---

## Commandes utiles

```bash
# Installer les dépendances
pip install scikit-learn fastapi uvicorn requests rich

# Lancer l'API (gardez ce terminal ouvert)
uvicorn 02_serve:app --host 0.0.0.0 --port 8000 --reload

# Dans un autre terminal : tester avec curl
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"texte": "Ce produit est excellent !"}'

# Vérifier l'état de l'API
curl http://localhost:8000/health

# Documentation interactive
# Ouvrir http://localhost:8000/docs dans le navigateur
```

---

## Bonus — Interface web

Si votre groupe a terminé avant la fin du temps imparti, créez `app/index.html`.

L'interface doit :
- Afficher une zone de texte pour saisir un avis
- Appeler `POST /predict` via `fetch()` en JavaScript
- Afficher le résultat (POSITIF / NÉGATIF + score)

L'API est déjà accessible sur `http://localhost:8000/predict`.
Pas besoin de backend supplémentaire — du HTML + JavaScript pur suffit.

---

*CITADEL · Frugal AI · Open Source · Ouagadougou, Burkina Faso · 2025*
