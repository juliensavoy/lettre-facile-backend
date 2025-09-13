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


# Modèles pour le générateur de discours de mariage

class SpeechRequest(BaseModel):
    """Modèle pour la requête de génération de discours de mariage"""
    prenom: str = Field(..., description="Prénom de la personne qui fait le discours")
    marie: str = Field(..., description="Nom de la personne qui se marie")
    partenaire: str = Field(..., description="Nom du/de la partenaire")
    lien: str = Field(..., description="Lien avec les mariés")
    style: Optional[str] = Field(None, description="Style du discours (optionnel)")
    qualites: Optional[str] = Field(None, description="Qualités du/de la marié(e) (optionnel)")
    anecdotes: Optional[str] = Field(None, description="Anecdotes à inclure (optionnel)")
    souvenir: Optional[str] = Field(None, description="Souvenir important à mentionner (optionnel)")
    rencontre: Optional[str] = Field(None, description="Comment ils se sont rencontrés (optionnel)")
    duree: Optional[str] = Field(None, description="Durée souhaitée du discours (optionnel)")


class SpeechResponse(BaseModel):
    """Modèle pour la réponse de génération de discours"""
    speech: str = Field(..., description="Contenu du discours généré")
    discours_id: Optional[str] = Field(None, description="ID du discours en base de données")


class SendSpeechRequest(BaseModel):
    """Modèle pour la requête d'envoi de discours par email"""
    email: EmailStr = Field(..., description="Email pour recevoir le discours")
    discours: str = Field(..., description="Contenu du discours à envoyer")


class SendSpeechResponse(BaseModel):
    """Modèle pour la réponse d'envoi de discours"""
    status: str = Field(..., description="Statut de l'envoi (success/error)")
    message: str = Field(..., description="Message d'information")


class GetSpeechResponse(BaseModel):
    """Modèle pour la réponse de récupération de discours"""
    discours: str = Field(..., description="Contenu du discours")
    created_at: str = Field(..., description="Date de création du discours") 