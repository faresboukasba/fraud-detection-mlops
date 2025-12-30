# 🖥️ Tester l'API Fraud Detection en Terminal

## 🎯 URL de Base
```
https://2sdeaedszk.eu-west-3.awsapprunner.com
```

---

## ✅ Test 1: Health Check (Vérifier que l'API fonctionne)

```bash
curl https://2sdeaedszk.eu-west-3.awsapprunner.com/health | jq .
```

**Résultat attendu:**
```json
{
  "status": "ok",
  "model_loaded": true
}
```

**Sans jq (affichage brut):**
```bash
curl https://2sdeaedszk.eu-west-3.awsapprunner.com/health
```

---

## 🔍 Test 2: Prédiction - Transaction Légitime (100€)

```bash
curl -X POST https://2sdeaedszk.eu-west-3.awsapprunner.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Time": 0,
    "Amount": 100,
    "V1": 0, "V2": 0, "V3": 0, "V4": 0, "V5": 0,
    "V6": 0, "V7": 0, "V8": 0, "V9": 0, "V10": 0,
    "V11": 0, "V12": 0, "V13": 0, "V14": 0, "V15": 0,
    "V16": 0, "V17": 0, "V18": 0, "V19": 0, "V20": 0,
    "V21": 0, "V22": 0, "V23": 0, "V24": 0, "V25": 0,
    "V26": 0, "V27": 0, "V28": 0,
    "amount_zscore": -0.048,
    "amount_log": 4.6052,
    "v1_v2_ratio": 0,
    "high_value": 0,
    "variance_all": 0,
    "max_abs_v": 0,
    "mean_abs_v": 0
  }' | jq .
```

**Résultat:**
```json
{
  "fraud": 0,
  "hybrid_score": 0.00000611,
  "threshold_used": 0.01
}
```

✅ **Légitime** - Score très faible (0.000006)

---

## 🚨 Test 3: Prédiction - Transaction Suspecte (10000€)

```bash
curl -X POST https://2sdeaedszk.eu-west-3.awsapprunner.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Time": 3600,
    "Amount": 9999.99,
    "V1": 2.5, "V2": -1.2, "V3": 1.8, "V4": -0.5, "V5": 0.7,
    "V6": -1.1, "V7": 0.9, "V8": -0.3, "V9": 1.2, "V10": -0.8,
    "V11": 0.4, "V12": -0.6, "V13": 1.5, "V14": -0.9, "V15": 0.2,
    "V16": -1.3, "V17": 0.6, "V18": -0.4, "V19": 1.1, "V20": -0.7,
    "V21": 0.8, "V22": -0.5, "V23": 0.3, "V24": -1.0, "V25": 0.5,
    "V26": -0.2, "V27": 0.9, "V28": -0.6,
    "amount_zscore": 39.96,
    "amount_log": 9.210,
    "v1_v2_ratio": 2.083,
    "high_value": 1,
    "variance_all": 0.747,
    "max_abs_v": 2.5,
    "mean_abs_v": 0.807
  }' | jq .
```

**Résultat:**
```json
{
  "fraud": 0,
  "hybrid_score": 0.00001589,
  "threshold_used": 0.01
}
```

⚠️ **Score modéré** - À analyser selon le contexte

---

## 💰 Test 4: Prédiction - Micro-paiement (0.50€)

```bash
curl -X POST https://2sdeaedszk.eu-west-3.awsapprunner.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Time": 1800,
    "Amount": 0.50,
    "V1": 0, "V2": 0, "V3": 0, "V4": 0, "V5": 0,
    "V6": 0, "V7": 0, "V8": 0, "V9": 0, "V10": 0,
    "V11": 0, "V12": 0, "V13": 0, "V14": 0, "V15": 0,
    "V16": 0, "V17": 0, "V18": 0, "V19": 0, "V20": 0,
    "V21": 0, "V22": 0, "V23": 0, "V24": 0, "V25": 0,
    "V26": 0, "V27": 0, "V28": 0,
    "amount_zscore": -0.349,
    "amount_log": 0.405,
    "v1_v2_ratio": 0,
    "high_value": 0,
    "variance_all": 0,
    "max_abs_v": 0,
    "mean_abs_v": 0
  }' | jq .
```

**Résultat:**
```json
{
  "fraud": 0,
  "hybrid_score": 0.00000001,
  "threshold_used": 0.01
}
```

✅ **Très légitime** - Score extrêmement faible

---

## 📋 Format de Réponse

Tous les tests retournent:
```json
{
  "fraud": 0,                      // 0 = légitime, 1 = fraude
  "hybrid_score": 0.00000611,      // Score entre 0 et 1
  "threshold_used": 0.01            // Seuil de classification
}
```

---

## 🔧 Commandes Utiles

### Installer jq (pour un affichage formaté)
```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# Windows (via chocolatey)
choco install jq
```

### Vérifier que jq est installé
```bash
jq --version
```

### Tester sans jq (affichage brut)
```bash
curl https://2sdeaedszk.eu-west-3.awsapprunner.com/health
```

### Sauvegarder la réponse dans un fichier
```bash
curl -X POST https://2sdeaedszk.eu-west-3.awsapprunner.com/predict \
  -H "Content-Type: application/json" \
  -d '{ ... }' > response.json

cat response.json | jq .
```

### Mesurer le temps de réponse
```bash
time curl https://2sdeaedszk.eu-west-3.awsapprunner.com/health
```

---

## ⚡ Commandes One-Liner Rapides

### Health Check Rapide
```bash
curl -s https://2sdeaedszk.eu-west-3.awsapprunner.com/health | jq '.status'
```

### Prédiction Légitime (copie-colle directe)
```bash
curl -s -X POST https://2sdeaedszk.eu-west-3.awsapprunner.com/predict -H "Content-Type: application/json" -d '{"Time":0,"Amount":100,"V1":0,"V2":0,"V3":0,"V4":0,"V5":0,"V6":0,"V7":0,"V8":0,"V9":0,"V10":0,"V11":0,"V12":0,"V13":0,"V14":0,"V15":0,"V16":0,"V17":0,"V18":0,"V19":0,"V20":0,"V21":0,"V22":0,"V23":0,"V24":0,"V25":0,"V26":0,"V27":0,"V28":0,"amount_zscore":-0.048,"amount_log":4.6052,"v1_v2_ratio":0,"high_value":0,"variance_all":0,"max_abs_v":0,"mean_abs_v":0}' | jq '.'
```

---

## 🐍 Python (Alternative)

Si vous préférez Python:

```python
import requests
import json

API = "https://2sdeaedszk.eu-west-3.awsapprunner.com"

# Health Check
print("Health Check:")
r = requests.get(f"{API}/health")
print(json.dumps(r.json(), indent=2))

# Prédiction
print("\nPrédiction:")
data = {
    "Time": 0, "Amount": 100,
    "V1": 0, "V2": 0, "V3": 0, "V4": 0, "V5": 0,
    "V6": 0, "V7": 0, "V8": 0, "V9": 0, "V10": 0,
    "V11": 0, "V12": 0, "V13": 0, "V14": 0, "V15": 0,
    "V16": 0, "V17": 0, "V18": 0, "V19": 0, "V20": 0,
    "V21": 0, "V22": 0, "V23": 0, "V24": 0, "V25": 0,
    "V26": 0, "V27": 0, "V28": 0,
    "amount_zscore": -0.048,
    "amount_log": 4.6052,
    "v1_v2_ratio": 0,
    "high_value": 0,
    "variance_all": 0,
    "max_abs_v": 0,
    "mean_abs_v": 0
}
r = requests.post(f"{API}/predict", json=data)
print(json.dumps(r.json(), indent=2))
```

Exécution:
```bash
python3 script.py
```

---

## 🧪 Résumé des Tests

| Test | Commande | Résultat Attendu |
|------|----------|------------------|
| Health | `curl https://2s.../health` | `"status": "ok"` |
| Légitime | `curl -X POST ... -d '{...}'` | `"fraud": 0` |
| Suspecte | `curl -X POST ... -d '{...}'` | `"fraud": 0 ou 1` |
| Micro | `curl -X POST ... -d '{...}'` | `"fraud": 0` |

---

## 📝 Notes Importantes

1. **Toutes les 37 features** doivent être présentes:
   - 30 primaires: Time, Amount, V1-V28
   - 7 dérivées: amount_zscore, amount_log, v1_v2_ratio, high_value, variance_all, max_abs_v, mean_abs_v

2. **Seuil:** 0.01 (très sensible)

3. **Réponse rapide:** Généralement < 500ms

4. **Accessible 24/7** tant que l'App Runner tourne

---

## 🆘 Dépannage

### Erreur "command not found: jq"
```bash
# Installez jq ou utilisez sans jq:
curl https://2sdeaedszk.eu-west-3.awsapprunner.com/health
```

### Erreur "Connection refused"
- Vérifiez que l'API est en ligne (health check)
- Vérifiez votre connexion internet
- Attendez quelques secondes et réessayez

### Erreur "Missing features"
- Assurez-vous que les 37 features sont présentes
- Vérifiez le JSON (utiliser https://jsonlint.com)

### Erreur "Invalid JSON"
- Vérifiez les guillemets
- Utilisez `python3 -m json.tool` pour valider:
  ```bash
  echo '{ "test": 1 }' | python3 -m json.tool
  ```

---

## ✅ Étapes Rapides

```bash
# 1. Test Health
curl https://2sdeaedszk.eu-west-3.awsapprunner.com/health

# 2. Test Prédiction (copie-colle Test 2 ci-dessus)

# 3. Voir le résultat
# {"fraud":0,"hybrid_score":0.00000611,"threshold_used":0.01}
```

**Prêt à tester!** 🚀

