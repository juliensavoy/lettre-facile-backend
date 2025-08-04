# Lettre Facile Backend

Backend FastAPI pour la génération automatique de lettres avec OpenAI et envoi par email.

## 🚀 Fonctionnalités

- Génération de lettres professionnelles avec OpenAI (GPT-3.5-turbo)
- Trois tons disponibles : formel, neutre, concis
- Envoi automatique par email (HTML et texte)
- API REST complète avec documentation automatique
- Gestion d'erreurs robuste
- Prêt pour le déploiement sur Render

## 📋 Prérequis

- Python 3.10+
- Compte OpenAI avec clé API
- Compte email avec accès SMTP (Gmail, Infomaniak, etc.)

## 🛠️ Installation

1. **Cloner le projet**
```bash
git clone <votre-repo>
cd lettre-facile-backend
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
cp env.example .env
```

Éditez le fichier `.env` avec vos informations :
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# SMTP Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Application Configuration
APP_NAME=Lettre Facile Backend
APP_VERSION=1.0.0
```

## 🔧 Configuration SMTP

### Gmail
- `SMTP_SERVER=smtp.gmail.com`
- `SMTP_PORT=587`
- Utilisez un "mot de passe d'application" (pas votre mot de passe principal)

### Infomaniak
- `SMTP_SERVER=mail.infomaniak.com`
- `SMTP_PORT=587`

## 🚀 Lancement

### Développement
```bash
python main.py
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

L'API sera disponible sur `http://localhost:8000`

## 📚 Documentation API

Une fois l'application lancée, accédez à :
- **Swagger UI** : `http://localhost:8000/docs`
- **ReDoc** : `http://localhost:8000/redoc`

## 🔌 Endpoints

### POST `/generate-letter`

Génère une lettre basée sur les informations fournies.

**Corps de la requête :**
```json
{
  "nom": "Jean Dupont",
  "adresse": "123 Rue de la Paix, 75001 Paris",
  "destinataire": "Monsieur Martin",
  "adresse_destinataire": "456 Avenue des Champs, 75008 Paris",
  "objet": "Demande de rendez-vous",
  "contexte": "Je souhaite prendre rendez-vous pour discuter d'un projet important.",
  "date_effet": "2024-01-15",
  "ton": "formel"
}
```

**Réponse :**
```json
{
  "lettre": "Contenu de la lettre générée...",
  "message": "Lettre générée avec succès"
}
```

### POST `/send-email`

Envoie une lettre par email.

**Corps de la requête :**
```json
{
  "lettre": "Contenu de la lettre à envoyer...",
  "email": "jean.dupont@email.com",
  "objet": "Demande de rendez-vous",
  "ton": "formel",
  "nom": "Jean Dupont",
  "destinataire": "Monsieur Martin"
}
```

**Réponse :**
```json
{
  "email_sent": true,
  "message": "Email envoyé avec succès"
}
```

### GET `/health`

Vérification de santé de l'API.

### GET `/`

Informations générales sur l'API.

## 🏗️ Structure du projet

```
lettre-facile-backend/
├── main.py              # Point d'entrée FastAPI
├── models.py            # Modèles Pydantic
├── letter.py            # Génération de lettres avec OpenAI
├── mailer.py            # Envoi d'emails SMTP
├── requirements.txt     # Dépendances Python
├── env.example          # Exemple de variables d'environnement
└── README.md           # Documentation
```

## 🚀 Déploiement sur Render

1. **Créer un nouveau service Web sur Render**
2. **Connecter votre repository Git**
3. **Configurer les variables d'environnement** dans l'interface Render
4. **Build Command** : `pip install -r requirements.txt`
5. **Start Command** : `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 🔒 Sécurité

- Toutes les clés API sont stockées dans des variables d'environnement
- Validation des données avec Pydantic
- Gestion d'erreurs sécurisée
- CORS configuré (à ajuster en production)

## 🐛 Dépannage

### Erreur "OPENAI_API_KEY non définie"
- Vérifiez que votre fichier `.env` existe et contient la clé API OpenAI

### Erreur d'authentification SMTP
- Vérifiez vos identifiants SMTP
- Pour Gmail, utilisez un "mot de passe d'application"

### Erreur de génération de lettre
- Vérifiez votre quota OpenAI
- Vérifiez la validité de votre clé API

## 📝 Licence

Ce projet est sous licence MIT.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request. 