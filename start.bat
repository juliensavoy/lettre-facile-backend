@echo off
REM Script de démarrage pour Lettre Facile Backend (Windows)

echo 🚀 Démarrage de Lettre Facile Backend...

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé. Veuillez l'installer d'abord.
    pause
    exit /b 1
)

REM Vérifier si le fichier .env existe
if not exist ".env" (
    echo ⚠️  Fichier .env non trouvé. Copie depuis env.example...
    copy env.example .env
    echo 📝 Veuillez configurer vos variables d'environnement dans le fichier .env
    echo    - OPENAI_API_KEY: Votre clé API OpenAI
    echo    - SMTP_*: Vos paramètres SMTP
)

REM Vérifier si l'environnement virtuel existe
if not exist "venv" (
    echo 📦 Création de l'environnement virtuel...
    python -m venv venv
)

REM Activer l'environnement virtuel
echo 🔧 Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer les dépendances
echo 📥 Installation des dépendances...
pip install -r requirements.txt

REM Démarrer l'application
echo 🌟 Démarrage de l'application...
echo 📚 Documentation disponible sur: http://localhost:8000/docs
echo 🔗 API disponible sur: http://localhost:8000
echo.
echo Appuyez sur Ctrl+C pour arrêter l'application
echo.

python main.py

pause 