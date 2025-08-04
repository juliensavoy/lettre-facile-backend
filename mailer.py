import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from typing import Optional


class EmailSender:
    """Classe pour envoyer des emails via SMTP"""
    
    def __init__(self):
        """Initialise la configuration SMTP pour Infomaniak"""
        # Configuration directe pour Infomaniak
        self.smtp_server = "mail.infomaniak.com"
        self.smtp_port = 465  # Port SSL pour Infomaniak
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        
        # Validation de la configuration
        if not all([self.smtp_username, self.smtp_password]):
            raise ValueError("SMTP_USERNAME et SMTP_PASSWORD doivent être définis dans les variables d'environnement")
    
    def _create_html_content(self, letter_content: str, request_data: dict) -> str:
        """Crée le contenu HTML de l'email"""
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Lettre générée - Lettre Facile</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    padding-bottom: 20px;
                    border-bottom: 2px solid #007bff;
                }}
                .header h1 {{
                    color: #007bff;
                    margin: 0;
                    font-size: 28px;
                }}
                .letter-content {{
                    background-color: #f8f9fa;
                    padding: 25px;
                    border-radius: 8px;
                    border-left: 4px solid #007bff;
                    white-space: pre-wrap;
                    font-family: 'Times New Roman', serif;
                    font-size: 14px;
                    line-height: 1.8;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                }}
                .info-box {{
                    background-color: #e3f2fd;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }}
                .info-box h3 {{
                    margin: 0 0 10px 0;
                    color: #1976d2;
                }}
                .info-box p {{
                    margin: 5px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📝 Lettre Facile</h1>
                    <p>Votre lettre a été générée avec succès</p>
                </div>
                
                <div class="info-box">
                    <h3>📋 Informations de la lettre</h3>
                    <p><strong>Objet :</strong> {request_data.get('objet', 'Non spécifié')}</p>
                    <p><strong>Ton :</strong> {request_data.get('ton', 'Non spécifié')}</p>
                    <p><strong>Date de génération :</strong> {formatdate(localtime=True)}</p>
                </div>
                
                <h3>📄 Contenu de votre lettre :</h3>
                <div class="letter-content">
{letter_content}
                </div>
                
                <div class="footer">
                    <p>Cette lettre a été générée automatiquement par Lettre Facile</p>
                    <p>Vous pouvez copier ce contenu et l'utiliser selon vos besoins</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def _create_text_content(self, letter_content: str, request_data: dict) -> str:
        """Crée le contenu texte de l'email"""
        
        text_content = f"""
Lettre Facile - Votre lettre a été générée

Informations de la lettre :
- Objet : {request_data.get('objet', 'Non spécifié')}
- Ton : {request_data.get('ton', 'Non spécifié')}
- Date de génération : {formatdate(localtime=True)}

Contenu de votre lettre :
{letter_content}

---
Cette lettre a été générée automatiquement par Lettre Facile
Vous pouvez copier ce contenu et l'utiliser selon vos besoins
        """
        
        return text_content.strip()
    
    async def send_letter_email(self, to_email: str, letter_content: str, request_data: dict) -> bool:
        """Envoie la lettre générée par email"""
        
        try:
            # Création du message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.smtp_username
            msg['To'] = to_email
            msg['Subject'] = f"Lettre générée - {request_data.get('objet', 'Lettre Facile')}"
            msg['Date'] = formatdate(localtime=True)
            
            # Contenu texte
            text_content = self._create_text_content(letter_content, request_data)
            text_part = MIMEText(text_content, 'plain', 'utf-8')
            msg.attach(text_part)
            
            # Contenu HTML
            html_content = self._create_html_content(letter_content, request_data)
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Connexion et envoi avec SSL (port 465)
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            return True
            
        except smtplib.SMTPAuthenticationError:
            raise Exception("Erreur d'authentification SMTP - vérifiez vos identifiants")
        except smtplib.SMTPRecipientsRefused:
            raise Exception("Adresse email destinataire invalide")
        except smtplib.SMTPServerDisconnected:
            raise Exception("Connexion au serveur SMTP perdue")
        except Exception as e:
            raise Exception(f"Erreur lors de l'envoi de l'email: {str(e)}") 