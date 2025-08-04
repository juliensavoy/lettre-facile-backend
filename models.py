from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum


class TonEnum(str, Enum):
    """Enumération pour les différents tons de lettre"""
    FORMEL = "formel"
    NEUTRE = "neutre"
    CONCIS = "concis"


class LetterRequest(BaseModel):
    """Modèle pour la requête de génération de lettre"""
    nom: str = Field(..., description="Nom de l'expéditeur")
    adresse: str = Field(..., description="Adresse de l'expéditeur")
    destinataire: str = Field(..., description="Nom du destinataire")
    adresse_destinataire: Optional[str] = Field(None, description="Adresse du destinataire (optionnel)")
    objet: str = Field(..., description="Objet de la lettre")
    contexte: str = Field(..., description="Contexte et détails de la lettre")
    date_effet: Optional[str] = Field(None, description="Date d'effet (optionnel)")
    ton: TonEnum = Field(..., description="Ton de la lettre (formel, neutre, concis)")


class EmailRequest(BaseModel):
    """Modèle pour la requête d'envoi d'email"""
    lettre: str = Field(..., description="Contenu de la lettre à envoyer")
    email: EmailStr = Field(..., description="Email pour recevoir la lettre")
    objet: str = Field(..., description="Objet de la lettre")
    ton: TonEnum = Field(..., description="Ton de la lettre")
    nom: str = Field(..., description="Nom de l'expéditeur")
    destinataire: str = Field(..., description="Nom du destinataire")
    letter_id: Optional[str] = Field(None, description="ID de la lettre en base de données (optionnel)")


class LetterResponse(BaseModel):
    """Modèle pour la réponse de génération de lettre"""
    lettre: str = Field(..., description="Contenu de la lettre générée")
    message: str = Field(..., description="Message d'information")
    letter_id: Optional[str] = Field(None, description="ID de la lettre en base de données")


class EmailResponse(BaseModel):
    """Modèle pour la réponse d'envoi d'email"""
    email_sent: bool = Field(..., description="Statut d'envoi de l'email")
    message: str = Field(..., description="Message d'information")


class ErrorResponse(BaseModel):
    """Modèle pour les réponses d'erreur"""
    error: str = Field(..., description="Message d'erreur")
    detail: Optional[str] = Field(None, description="Détails de l'erreur") 