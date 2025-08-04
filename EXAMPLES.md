# Exemples d'utilisation - Lettre Facile Backend

## 📝 Exemples de requêtes

### 1. Lettre de démission (Ton formel)

```json
{
  "nom": "Marie Dubois",
  "adresse": "15 Avenue Victor Hugo, 69002 Lyon",
  "destinataire": "Monsieur Jean Martin",
  "adresse_destinataire": "Direction des Ressources Humaines\nEntreprise ABC\n123 Boulevard de la République\n69001 Lyon",
  "objet": "Lettre de démission",
  "contexte": "Je souhaite démissionner de mon poste de développeuse web pour des raisons personnelles. Mon préavis est de 2 mois selon mon contrat.",
  "date_effet": "2024-02-15",
  "ton": "formel",
  "email": "marie.dubois@email.com"
}
```

### 2. Demande de rendez-vous (Ton neutre)

```json
{
  "nom": "Pierre Durand",
  "adresse": "8 Rue des Fleurs, 31000 Toulouse",
  "destinataire": "Docteur Sophie Bernard",
  "adresse_destinataire": "Cabinet Médical\n45 Rue de la Santé\n31000 Toulouse",
  "objet": "Demande de rendez-vous",
  "contexte": "Je souhaite prendre rendez-vous pour une consultation de routine. Je préférerais un créneau en matinée si possible.",
  "ton": "neutre",
  "email": "pierre.durand@email.com"
}
```

### 3. Réclamation client (Ton concis)

```json
{
  "nom": "Luc Moreau",
  "adresse": "22 Place du Commerce, 44000 Nantes",
  "destinataire": "Service Client",
  "adresse_destinataire": "Société XYZ\nService Client\n1 Rue de l'Industrie\n75001 Paris",
  "objet": "Réclamation - Commande #12345",
  "contexte": "Ma commande livrée le 10/01/2024 contient un article défectueux. Je demande un remboursement ou un échange.",
  "ton": "concis",
  "email": "luc.moreau@email.com"
}
```

### 4. Lettre de motivation (Ton formel)

```json
{
  "nom": "Emma Rousseau",
  "adresse": "3 Impasse des Lilas, 13001 Marseille",
  "destinataire": "Madame Claire Dubois",
  "adresse_destinataire": "Directrice RH\nStartup Innovante\n78 Quai des Belges\n13001 Marseille",
  "objet": "Candidature - Poste de Data Analyst",
  "contexte": "Je postule au poste de Data Analyst que vous proposez. J'ai 3 ans d'expérience en analyse de données et maîtrise Python, SQL et Tableau. Je suis passionnée par l'innovation et souhaite rejoindre votre équipe dynamique.",
  "ton": "formel",
  "email": "emma.rousseau@email.com"
}
```

## 🔌 Endpoints API

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

## 🔧 Exemples de code client

### JavaScript (Fetch API) - Génération + Envoi séparés

```javascript
// 1. Génération de la lettre
async function generateLetter(letterData) {
    try {
        const response = await fetch('http://localhost:8000/generate-letter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(letterData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Lettre générée:', result.lettre);
        
        return result;
    } catch (error) {
        console.error('Erreur:', error);
        throw error;
    }
}

// 2. Envoi de l'email
async function sendEmail(emailData) {
    try {
        const response = await fetch('http://localhost:8000/send-email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(emailData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Email envoyé:', result.email_sent);
        
        return result;
    } catch (error) {
        console.error('Erreur:', error);
        throw error;
    }
}

// Utilisation en deux étapes
const letterData = {
    nom: "Jean Dupont",
    adresse: "123 Rue de la Paix, 75001 Paris",
    destinataire: "Monsieur Martin",
    adresse_destinataire: "456 Avenue des Champs, 75008 Paris",
    objet: "Demande de rendez-vous",
    contexte: "Je souhaite prendre rendez-vous pour discuter d'un projet important.",
    ton: "formel"
};

// Étape 1: Générer la lettre
generateLetter(letterData)
    .then(result => {
        // Afficher la lettre dans l'interface
        document.getElementById('letter-content').textContent = result.lettre;
        
        // Étape 2: Envoyer par email (optionnel)
        const emailData = {
            lettre: result.lettre,
            email: "jean.dupont@email.com",
            objet: letterData.objet,
            ton: letterData.ton,
            nom: letterData.nom,
            destinataire: letterData.destinataire
        };
        
        return sendEmail(emailData);
    })
    .then(emailResult => {
        console.log('Processus terminé:', emailResult.message);
    })
    .catch(error => {
        console.error('Erreur lors du processus:', error);
    });
```

### Python (requests) - Génération + Envoi séparés

```python
import requests
import json

def generate_letter(letter_data):
    """Génère une lettre via l'API"""
    
    url = "http://localhost:8000/generate-letter"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=letter_data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        print(f"Lettre générée ({len(result['lettre'])} caractères)")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête: {e}")
        raise

def send_email(email_data):
    """Envoie une lettre par email via l'API"""
    
    url = "http://localhost:8000/send-email"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=email_data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        print(f"Email envoyé: {result['email_sent']}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête: {e}")
        raise

# Exemple d'utilisation en deux étapes
letter_data = {
    "nom": "Sophie Martin",
    "adresse": "45 Rue du Commerce, 59000 Lille",
    "destinataire": "Monsieur le Maire",
    "adresse_destinataire": "Hôtel de Ville\nPlace du Général de Gaulle\n59000 Lille",
    "objet": "Demande d'autorisation d'événement",
    "contexte": "Je souhaite organiser un marché artisanal dans le parc municipal le 15 juin 2024.",
    "ton": "formel"
}

# Étape 1: Générer la lettre
result = generate_letter(letter_data)
print("Contenu de la lettre:")
print(result['lettre'])

# Étape 2: Envoyer par email (optionnel)
email_data = {
    "lettre": result['lettre'],
    "email": "sophie.martin@email.com",
    "objet": letter_data['objet'],
    "ton": letter_data['ton'],
    "nom": letter_data['nom'],
    "destinataire": letter_data['destinataire']
}

email_result = send_email(email_data)
print(f"Processus terminé: {email_result['message']}")
```

### cURL - Génération + Envoi séparés

```bash
# 1. Génération de la lettre
curl -X POST "http://localhost:8000/generate-letter" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Thomas Leroy",
    "adresse": "12 Rue de la Liberté, 21000 Dijon",
    "destinataire": "Service Client",
    "adresse_destinataire": "Banque Populaire\nService Client\n1 Place de la République\n21000 Dijon",
    "objet": "Demande de modification de RIB",
    "contexte": "Je souhaite modifier mon RIB pour mes prélèvements automatiques.",
    "ton": "neutre"
  }'

# 2. Envoi de l'email (utiliser la lettre générée ci-dessus)
curl -X POST "http://localhost:8000/send-email" \
  -H "Content-Type: application/json" \
  -d '{
    "lettre": "Contenu de la lettre générée...",
    "email": "thomas.leroy@email.com",
    "objet": "Demande de modification de RIB",
    "ton": "neutre",
    "nom": "Thomas Leroy",
    "destinataire": "Service Client"
  }'
```

## 📧 Exemples d'emails reçus

### Email HTML (extrait)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <title>Lettre générée - Lettre Facile</title>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 Lettre Facile</h1>
            <p>Votre lettre a été générée avec succès</p>
        </div>
        
        <div class="info-box">
            <h3>📋 Informations de la lettre</h3>
            <p><strong>Objet :</strong> Lettre de démission</p>
            <p><strong>Ton :</strong> formel</p>
            <p><strong>Date de génération :</strong> 15 janvier 2024</p>
        </div>
        
        <h3>📄 Contenu de votre lettre :</h3>
        <div class="letter-content">
            [Contenu de la lettre générée]
        </div>
    </div>
</body>
</html>
```

## 🚀 Tests avec l'API

### Test de santé

```bash
curl http://localhost:8000/health
```

Réponse attendue :
```json
{
  "status": "healthy",
  "services": {
    "openai": "configured",
    "smtp": "configured"
  }
}
```

### Test avec données invalides

```bash
curl -X POST "http://localhost:8000/generate-letter" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Test",
    "ton": "formel"
  }'
```

Réponse attendue (erreur de validation) :
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## 💡 Conseils d'utilisation

1. **Ton formel** : Pour les lettres officielles, démissions, réclamations importantes
2. **Ton neutre** : Pour les demandes de rendez-vous, questions générales
3. **Ton concis** : Pour les réclamations simples, demandes rapides

4. **Contexte** : Plus le contexte est détaillé, meilleure sera la lettre générée
5. **Date d'effet** : Optionnel, mais utile pour les lettres avec échéance
6. **Email** : Assurez-vous que l'adresse email est valide pour recevoir la lettre 