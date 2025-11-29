# fraud-detection-mlops
Voici un **README.md** prêt à copier-coller dans ton repo GitHub :

```markdown
#  MLOps – Détection de Fraude Bancaire

Un projet complet de **détection de fraude bancaire** avec pipelines automatisés, modèle optimisé et API déployée sur AWS ECS.

---

##  Structure du projet

```

src/
├─ data/
├─ model/
├─ notebooks/
models/
api/

````

- Notebook et code ML : **BOA + XGBoost**
- Modèle final sauvegardé : `models/model.pkl`

---

##  Data Pipeline

- **download_data.py** → importer dataset (Kaggle → local → S3)  
- **clean_transform.py** → nettoyage, normalisation, SMOTE  
- **load_final.py** → sauvegarde en Parquet  
- **data_pipeline.py** → orchestrateur des étapes

---

##  Model Pipeline

- Charger les données finales  
- Entraîner **XGBoost + SMOTE + BOA**  
- Générer métriques : ROC-AUC, PR-AUC, F1  
- Sauvegarder le modèle : `models/model.pkl`

---

##  API FastAPI

- Fichier : `api/app.py`  
- Endpoints :
  - `/health` → vérifier service
  - `/predict` → prédire fraude  
- Modèle chargé avec : `joblib.load("models/model.pkl")`

---

##  Dockerisation

- **Dockerfile** : copier code, installer dépendances, lancer API  
- Construire et lancer :

```bash
docker build -t fraud-api .
docker run -p 8000:8000 fraud-api
````

---

##  Déploiement AWS

* **S3** : bucket `groupeX-data` pour données
* **ECR** : repository `groupeX-mlops` pour Docker image
* **ECS Fargate** : cluster, service, task definition
* URL publique → accéder à l’API

---

##  CI/CD GitHub Actions

* `.github/workflows/deploy.yml` :

  * Login AWS
  * Build Docker image
  * Push vers ECR
  * Mise à jour ECS

---

##  Monitoring

* **CloudWatch** : logs API, erreurs, débit, temps de réponse

---

##  Résultat final

* Pipelines automatisés
* Modèle optimisé (BOA + XGBoost)
* API dockerisée et déployée sur AWS ECS
* Monitoring via CloudWatch

```

