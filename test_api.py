#!/usr/bin/env python3
"""
Script de test pour l'API Lettre Facile Backend
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test@example.com"  # Remplacez par votre email de test

def test_health_check():
    """Test de l'endpoint de santé"""
    print("🔍 Test de l'endpoint de santé...")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Endpoint de santé OK")
            print(f"   Réponse: {response.json()}")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'API. Assurez-vous qu'elle est démarrée.")
        return False
    
    return True

def test_root_endpoint():
    """Test de l'endpoint racine"""
    print("\n🔍 Test de l'endpoint racine...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Endpoint racine OK")
            print(f"   Réponse: {response.json()}")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    return True

def test_generate_letter():
    """Test de génération de lettre"""
    print("\n🔍 Test de génération de lettre...")
    
    # Données de test
    test_data = {
        "nom": "Jean Dupont",
        "adresse": "123 Rue de la Paix, 75001 Paris",
        "destinataire": "Monsieur Martin",
        "adresse_destinataire": "456 Avenue des Champs, 75008 Paris",
        "objet": "Demande de rendez-vous",
        "contexte": "Je souhaite prendre rendez-vous pour discuter d'un projet important concernant le développement de notre application web.",
        "date_effet": "2024-01-15",
        "ton": "formel"
    }
    
    try:
        print("   Envoi de la requête...")
        response = requests.post(
            f"{BASE_URL}/generate-letter",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Génération de lettre réussie!")
            print(f"   Message: {result.get('message', '')}")
            print(f"   Longueur de la lettre: {len(result.get('lettre', ''))} caractères")
            
            # Afficher un extrait de la lettre
            lettre = result.get('lettre', '')
            if lettre:
                print(f"   Extrait de la lettre:\n{lettre[:200]}...")
            
            # Retourner la lettre générée pour le test d'envoi
            return result.get('lettre', '')
            
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   Détails: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
    
    return None


def test_send_email(lettre_generée=None):
    """Test d'envoi d'email"""
    print("\n🔍 Test d'envoi d'email...")
    
    # Si aucune lettre n'est fournie, utiliser un exemple
    if not lettre_generée:
        lettre_generée = """Monsieur Martin,

Je me permets de vous contacter concernant une demande de rendez-vous.

Cordialement,
Jean Dupont"""
    
    # Données de test pour l'envoi d'email
    test_data = {
        "lettre": lettre_generée,
        "email": TEST_EMAIL,
        "objet": "Demande de rendez-vous",
        "ton": "formel",
        "nom": "Jean Dupont",
        "destinataire": "Monsieur Martin"
    }
    
    try:
        print("   Envoi de la requête...")
        response = requests.post(
            f"{BASE_URL}/send-email",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Envoi d'email réussi!")
            print(f"   Email envoyé: {result.get('email_sent', False)}")
            print(f"   Message: {result.get('message', '')}")
            
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   Détails: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
    
    return True

def test_invalid_request():
    """Test avec des données invalides"""
    print("\n🔍 Test avec des données invalides...")
    
    # Données invalides (email manquant)
    invalid_data = {
        "nom": "Jean Dupont",
        "adresse": "123 Rue de la Paix",
        "destinataire": "Monsieur Martin",
        "adresse_destinataire": "456 Avenue des Champs",
        "objet": "Test",
        "contexte": "Test de validation",
        "ton": "formel"
        # email manquant intentionnellement
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-letter",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 422:  # Validation error
            print("✅ Validation des données OK (erreur attendue)")
        else:
            print(f"❌ Réponse inattendue: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

def main():
    """Fonction principale de test"""
    print("🚀 Démarrage des tests de l'API Lettre Facile Backend")
    print("=" * 60)
    
    # Tests de base
    if not test_health_check():
        return
    
    test_root_endpoint()
    
    # Test de génération (optionnel - nécessite une clé OpenAI valide)
    print("\n⚠️  Le test de génération nécessite une clé OpenAI valide.")
    print("   Si vous n'en avez pas, ce test échouera mais c'est normal.")
    
    user_input = input("\nVoulez-vous tester la génération de lettre? (o/n): ")
    lettre_generée = None
    if user_input.lower() in ['o', 'oui', 'y', 'yes']:
        lettre_generée = test_generate_letter()
    
    # Test d'envoi d'email
    print("\n⚠️  Le test d'envoi d'email nécessite une configuration SMTP valide.")
    user_input = input("Voulez-vous tester l'envoi d'email? (o/n): ")
    if user_input.lower() in ['o', 'oui', 'y', 'yes']:
        test_send_email(lettre_generée)
    
    # Test de validation
    test_invalid_request()
    
    print("\n" + "=" * 60)
    print("✅ Tests terminés!")
    print("\n📚 Documentation disponible sur:")
    print(f"   - Swagger UI: {BASE_URL}/docs")
    print(f"   - ReDoc: {BASE_URL}/redoc")

if __name__ == "__main__":
    main() 