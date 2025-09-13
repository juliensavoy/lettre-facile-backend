import os
from typing import Optional, Dict, Any
from supabase import create_client, Client
from datetime import datetime


class DatabaseManager:
    """Gestionnaire de base de données Supabase"""
    
    def __init__(self):
        """Initialise la connexion à Supabase"""
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL et SUPABASE_ANON_KEY doivent être définis dans les variables d'environnement")
        
        self.supabase: Client = create_client(supabase_url, supabase_key)
    
    async def save_letter(self, letter_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sauvegarde une lettre dans la base de données
        
        Args:
            letter_data: Dictionnaire contenant les données de la lettre
            
        Returns:
            Dictionnaire avec l'ID de la lettre créée
        """
        try:
            # Préparation des données pour l'insertion
            insert_data = {
                "nom": letter_data["nom"],
                "adresse": letter_data["adresse"],
                "destinataire": letter_data["destinataire"],
                "adresse_destinataire": letter_data.get("adresse_destinataire"),
                "objet": letter_data["objet"],
                "contexte": letter_data["contexte"],
                "date_effet": letter_data.get("date_effet"),
                "ton": letter_data["ton"],
                "lettre_generée": letter_data["lettre_generée"],
                "email_destinataire": letter_data.get("email_destinataire"),
                "email_envoye": letter_data.get("email_envoye", False)
            }
            
            # Insertion dans la base de données
            result = self.supabase.table("letters").insert(insert_data).execute()
            
            if result.data:
                return {
                    "success": True,
                    "letter_id": result.data[0]["id"],
                    "message": "Lettre sauvegardée avec succès"
                }
            else:
                raise Exception("Aucune donnée retournée lors de l'insertion")
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la sauvegarde: {str(e)}"
            }
    
    async def update_email_status(self, letter_id: str, email_sent: bool, email_destinataire: str = None) -> Dict[str, Any]:
        """
        Met à jour le statut d'envoi d'email d'une lettre
        
        Args:
            letter_id: ID de la lettre
            email_sent: Statut d'envoi
            email_destinataire: Adresse email du destinataire (optionnel)
            
        Returns:
            Dictionnaire avec le résultat de la mise à jour
        """
        try:
            update_data = {
                "email_envoye": email_sent,
                "updated_at": datetime.now().isoformat()
            }
            
            # Ajouter l'email du destinataire si fourni
            if email_destinataire:
                update_data["email_destinataire"] = email_destinataire
            
            result = self.supabase.table("letters").update(update_data).eq("id", letter_id).execute()
            
            if result.data:
                return {
                    "success": True,
                    "message": "Statut d'email mis à jour avec succès"
                }
            else:
                raise Exception("Lettre non trouvée")
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la mise à jour: {str(e)}"
            }
    
    async def get_letter_by_id(self, letter_id: str) -> Dict[str, Any]:
        """
        Récupère une lettre par son ID
        
        Args:
            letter_id: ID de la lettre
            
        Returns:
            Dictionnaire avec les données de la lettre
        """
        try:
            result = self.supabase.table("letters").select("*").eq("id", letter_id).execute()
            
            if result.data:
                return {
                    "success": True,
                    "letter": result.data[0]
                }
            else:
                return {
                    "success": False,
                    "error": "Lettre non trouvée"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la récupération: {str(e)}"
            }
    
    async def get_recent_letters(self, limit: int = 10) -> Dict[str, Any]:
        """
        Récupère les lettres récentes
        
        Args:
            limit: Nombre de lettres à récupérer
            
        Returns:
            Dictionnaire avec la liste des lettres
        """
        try:
            result = self.supabase.table("letters").select("*").order("created_at", desc=True).limit(limit).execute()
            
            return {
                "success": True,
                "letters": result.data,
                "count": len(result.data)
            }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la récupération: {str(e)}"
            }
    
    async def get_letters_by_email(self, email: str) -> Dict[str, Any]:
        """
        Récupère toutes les lettres envoyées à un email
        
        Args:
            email: Adresse email
            
        Returns:
            Dictionnaire avec la liste des lettres
        """
        try:
            result = self.supabase.table("letters").select("*").eq("email_destinataire", email).order("created_at", desc=True).execute()
            
            return {
                "success": True,
                "letters": result.data,
                "count": len(result.data)
            }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la récupération: {str(e)}"
            }
    
    async def find_letter_by_content(self, content_start: str) -> Dict[str, Any]:
        """
        Trouve une lettre par le début de son contenu
        
        Args:
            content_start: Début du contenu de la lettre
            
        Returns:
            Dictionnaire avec les données de la lettre
        """
        try:
            # Recherche de lettres contenant ce début de contenu
            result = self.supabase.table("letters").select("*").ilike("lettre_generée", f"{content_start}%").order("created_at", desc=True).limit(1).execute()
            
            if result.data:
                return {
                    "success": True,
                    "letter": result.data[0]
                }
            else:
                return {
                    "success": False,
                    "error": "Aucune lettre trouvée avec ce contenu"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la recherche: {str(e)}"
            }
    
    # Méthodes pour les discours de mariage
    
    async def save_speech(self, speech_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sauvegarde un discours de mariage dans la base de données
        
        Args:
            speech_data: Dictionnaire contenant les données du discours
            
        Returns:
            Dictionnaire avec l'ID du discours créé
        """
        try:
            # Préparation des données pour l'insertion
            insert_data = {
                "prenom": speech_data["prenom"],
                "marie": speech_data["marie"],
                "partenaire": speech_data["partenaire"],
                "style": speech_data.get("style"),
                "lien": speech_data["lien"],
                "rencontre": speech_data.get("rencontre"),
                "qualites": speech_data.get("qualites"),
                "anecdotes": speech_data.get("anecdotes"),
                "souvenirs": speech_data.get("souvenir"),  # Note: "souvenir" dans les données, "souvenirs" en base
                "duree": speech_data.get("duree"),
                "discours": speech_data["discours"]
            }
            
            # Insertion dans la base de données
            result = self.supabase.table("discours_mariage").insert(insert_data).execute()
            
            if result.data:
                return {
                    "success": True,
                    "speech_id": result.data[0]["id"],
                    "message": "Discours sauvegardé avec succès"
                }
            else:
                raise Exception("Aucune donnée retournée lors de l'insertion")
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la sauvegarde: {str(e)}"
            }
    
    async def get_speech_by_id(self, speech_id: str) -> Dict[str, Any]:
        """
        Récupère un discours par son ID
        
        Args:
            speech_id: ID du discours
            
        Returns:
            Dictionnaire avec les données du discours
        """
        try:
            result = self.supabase.table("discours_mariage").select("discours, created_at").eq("id", speech_id).execute()
            
            if result.data:
                return {
                    "success": True,
                    "speech": result.data[0]
                }
            else:
                return {
                    "success": False,
                    "error": "Discours non trouvé"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la récupération: {str(e)}"
            }