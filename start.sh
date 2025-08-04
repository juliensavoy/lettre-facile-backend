#!/bin/bash

# Script de démarrage pour Lettre Facile Backend

echo "🚀 Démarrage de Lettre Facile Backend..."

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si le fichier .env existe
if [ ! -f ".env" ]; then
    echo "⚠️  Fichier .env non trouvé. Copie depuis env.example..."
    cp env.example .env
    echo "📝 Veuillez configurer vos variables d'environnement dans le fichier .env"
    echo "   - OPENAI_API_KEY: Votre clé API OpenAI"
    echo "   - SMTP_*: Vos paramètres SMTP"
fi

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install -r requirements.txt

# Démarrer l'application
echo "🌟 Démarrage de l'application..."
echo "📚 Documentation disponible sur: http://localhost:8000/docs"
echo "🔗 API disponible sur: http://localhost:8000"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter l'application"
echo ""

python main.py 