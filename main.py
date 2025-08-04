import os
import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import uvicorn

from models import LetterRequest, LetterResponse, EmailRequest, EmailResponse, ErrorResponse
from letter import LetterGenerator
from mailer import EmailSender
from database import DatabaseManager

# Chargement des variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="Lettre Facile Backend",
    description="API pour la génération automatique de lettres avec OpenAI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifiez les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation des services
letter_generator = None
email_sender = None
database_manager = None

@app.on_event("startup")
async def startup_event():
    """Initialise les services au démarrage de l'application"""
    global letter_generator, email_sender, database_manager
    
    try:
        # Vérification des variables d'environnement
        required_vars = [
            "OPENAI_API_KEY",
            "SMTP_USERNAME",
            "SMTP_PASSWORD",
            "SUPABASE_URL",
            "SUPABASE_ANON_KEY"
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            logger.error(f"Variables d'environnement manquantes: {missing_vars}")
            raise ValueError(f"Variables d'environnement manquantes: {missing_vars}")
        
        # Initialisation des services
        letter_generator = LetterGenerator()
        email_sender = EmailSender()
        database_manager = DatabaseManager()
        
        logger.info("Application démarrée avec succès")
        
    except Exception as e:
        logger.error(f"Erreur lors du démarrage: {str(e)}")
        raise e

@app.get("/", tags=["Health"])
async def root():
    """Point d'entrée principal - vérification de santé de l'API"""
    return {
        "message": "Lettre Facile Backend API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint de vérification de santé"""
    return {
        "status": "healthy",
        "services": {
            "openai": "configured" if letter_generator else "not_configured",
            "smtp": "configured" if email_sender else "not_configured",
            "database": "configured" if database_manager else "not_configured"
        }
    }

@app.post("/generate-letter", 
          response_model=LetterResponse,
          responses={
              400: {"model": ErrorResponse},
              500: {"model": ErrorResponse}
          },
          tags=["Letters"])
async def generate_letter(request: LetterRequest):
    """
    Génère une lettre basée sur les informations fournies.
    
    - **nom**: Nom de l'expéditeur
    - **adresse**: Adresse de l'expéditeur
    - **destinataire**: Nom du destinataire
    - **adresse_destinataire**: Adresse du destinataire
    - **objet**: Objet de la lettre
    - **contexte**: Contexte et détails de la lettre
    - **date_effet**: Date d'effet (optionnel)
    - **ton**: Ton de la lettre (formel, neutre, concis)
    """
    
    try:
        logger.info(f"Début de génération de lettre")
        
        # Génération de la lettre
        letter_content = await letter_generator.generate_letter(request)
        logger.info("Lettre générée avec succès")
        
        # Sauvegarde en base de données
        letter_id = None
        try:
            letter_data = {
                "nom": request.nom,
                "adresse": request.adresse,
                "destinataire": request.destinataire,
                "adresse_destinataire": request.adresse_destinataire,
                "objet": request.objet,
                "contexte": request.contexte,
                "date_effet": request.date_effet,
                "ton": request.ton.value,
                "lettre_generée": letter_content,
                "email_destinataire": None,
                "email_envoye": False
            }
            
            db_result = await database_manager.save_letter(letter_data)
            if db_result["success"]:
                letter_id = db_result["letter_id"]
                logger.info(f"Lettre sauvegardée en base avec l'ID: {letter_id}")
            else:
                logger.warning(f"Erreur lors de la sauvegarde en base: {db_result['error']}")
                
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde en base: {str(e)}")
        
        return LetterResponse(
            lettre=letter_content,
            message="Lettre générée avec succès",
            letter_id=letter_id
        )
        
    except ValueError as e:
        logger.error(f"Erreur de validation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Erreur lors de la génération de lettre: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur interne du serveur: {str(e)}"
        )


@app.post("/send-email", 
          response_model=EmailResponse,
          responses={
              400: {"model": ErrorResponse},
              500: {"model": ErrorResponse}
          },
          tags=["Email"])
async def send_email(request: EmailRequest):
    """
    Envoie une lettre par email.
    
    - **lettre**: Contenu de la lettre à envoyer
    - **email**: Email pour recevoir la lettre
    - **objet**: Objet de la lettre
    - **ton**: Ton de la lettre
    - **nom**: Nom de l'expéditeur
    - **destinataire**: Nom du destinataire
    - **letter_id**: ID de la lettre (optionnel, sinon recherche automatique)
    """
    
    try:
        logger.info(f"Début d'envoi d'email à {request.email}")
        
        # Préparation des données pour l'email
        request_data = {
            "objet": request.objet,
            "ton": request.ton.value,
            "nom": request.nom,
            "destinataire": request.destinataire
        }
        
        # Envoi de l'email
        email_sent = False
        try:
            await email_sender.send_letter_email(
                to_email=request.email,
                letter_content=request.lettre,
                request_data=request_data
            )
            email_sent = True
            logger.info(f"Email envoyé avec succès à {request.email}")
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email: {str(e)}")
            raise e
        
        # Recherche et mise à jour du statut en base de données
        letter_id_to_update = request.letter_id
        
        # Si pas de letter_id fourni, essayer de trouver la lettre par contenu
        if not letter_id_to_update:
            try:
                # Recherche de la lettre la plus récente avec ce contenu
                result = await database_manager.find_letter_by_content(request.lettre[:100])  # Premiers 100 caractères
                if result["success"] and result["letter"]:
                    letter_id_to_update = result["letter"]["id"]
                    logger.info(f"Lettre trouvée automatiquement: {letter_id_to_update}")
            except Exception as e:
                logger.warning(f"Impossible de trouver la lettre automatiquement: {str(e)}")
        
        # Mise à jour du statut si on a un letter_id
        if letter_id_to_update:
            try:
                await database_manager.update_email_status(letter_id_to_update, email_sent, request.email)
                logger.info(f"Statut d'email mis à jour en base pour la lettre {letter_id_to_update}")
            except Exception as e:
                logger.warning(f"Erreur lors de la mise à jour du statut: {str(e)}")
        
        return EmailResponse(
            email_sent=email_sent,
            message="Email envoyé avec succès" if email_sent else "Erreur lors de l'envoi de l'email"
        )
        
    except ValueError as e:
        logger.error(f"Erreur de validation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur interne du serveur: {str(e)}"
        )


@app.get("/letters", 
          responses={
              500: {"model": ErrorResponse}
          },
          tags=["Letters"])
async def get_recent_letters(limit: int = 10):
    """
    Récupère les lettres récentes.
    
    - **limit**: Nombre de lettres à récupérer (défaut: 10)
    """
    
    try:
        result = await database_manager.get_recent_letters(limit)
        
        if result["success"]:
            return {
                "letters": result["letters"],
                "count": result["count"],
                "message": f"{result['count']} lettres récupérées"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des lettres: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur interne du serveur: {str(e)}"
        )


@app.get("/letters/{letter_id}", 
          responses={
              404: {"model": ErrorResponse},
              500: {"model": ErrorResponse}
          },
          tags=["Letters"])
async def get_letter_by_id(letter_id: str):
    """
    Récupère une lettre par son ID.
    
    - **letter_id**: ID de la lettre
    """
    
    try:
        result = await database_manager.get_letter_by_id(letter_id)
        
        if result["success"]:
            return {
                "letter": result["letter"],
                "message": "Lettre récupérée avec succès"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la lettre: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur interne du serveur: {str(e)}"
        )


@app.get("/letters/email/{email}", 
          responses={
              500: {"model": ErrorResponse}
          },
          tags=["Letters"])
async def get_letters_by_email(email: str):
    """
    Récupère toutes les lettres envoyées à un email.
    
    - **email**: Adresse email
    """
    
    try:
        result = await database_manager.get_letters_by_email(email)
        
        if result["success"]:
            return {
                "letters": result["letters"],
                "count": result["count"],
                "message": f"{result['count']} lettres trouvées pour {email}"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des lettres par email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur interne du serveur: {str(e)}"
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Gestionnaire d'erreurs HTTP personnalisé"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Gestionnaire d'erreurs général"""
    logger.error(f"Erreur non gérée: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Erreur interne du serveur",
            "detail": str(exc) if os.getenv("DEBUG", "false").lower() == "true" else "Une erreur inattendue s'est produite"
        }
    )

if __name__ == "__main__":
    # Configuration pour le développement
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 