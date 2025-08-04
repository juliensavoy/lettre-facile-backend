import os
import openai
from typing import Optional
from models import LetterRequest, TonEnum


class LetterGenerator:
    """Classe pour générer des lettres avec OpenAI"""
    
    def __init__(self):
        """Initialise le client OpenAI avec la clé API"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY non définie dans les variables d'environnement")
        
        self.client = openai.OpenAI(api_key=api_key)
    
    def _build_prompt(self, request: LetterRequest) -> str:
        """Construit le prompt pour OpenAI basé sur les données de la requête"""
        
        # Instructions de base selon le ton
        ton_instructions = {
            TonEnum.FORMEL: "Utilisez un ton très formel et respectueux, avec des formules de politesse appropriées.",
            TonEnum.NEUTRE: "Utilisez un ton neutre et professionnel, équilibré entre formel et décontracté.",
            TonEnum.CONCIS: "Soyez concis et direct, allez droit au but sans fioritures."
        }
        
        # Construction du prompt
        prompt = f"""
Vous êtes un assistant spécialisé dans la rédaction de lettres professionnelles en français.

{ton_instructions[request.ton]}

Veuillez rédiger une lettre avec les informations suivantes :

**Expéditeur :**
- Nom : {request.nom}
- Adresse : {request.adresse}

**Destinataire :**
- Nom : {request.destinataire}
{f"- Adresse : {request.adresse_destinataire}" if request.adresse_destinataire else ""}

**Objet :** {request.objet}

**Contexte :** {request.contexte}

{f"**Date d'effet :** {request.date_effet}" if request.date_effet else ""}

Instructions spécifiques :
1. Formatez la lettre correctement avec en-tête, corps et signature
2. Incluez la date actuelle
3. Respectez les conventions de rédaction de lettres en français
4. Adaptez le contenu au contexte fourni
5. Assurez-vous que la lettre soit complète et prête à être envoyée

Générez uniquement le contenu de la lettre, sans commentaires supplémentaires.
"""
        
        return prompt.strip()
    
    async def generate_letter(self, request: LetterRequest) -> str:
        """Génère une lettre en utilisant l'API OpenAI"""
        
        try:
            prompt = self._build_prompt(request)
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Vous êtes un assistant spécialisé dans la rédaction de lettres professionnelles en français. Vous générez des lettres complètes et bien formatées."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            # Extraction du contenu généré
            generated_letter = response.choices[0].message.content.strip()
            
            if not generated_letter:
                raise ValueError("Aucun contenu généré par OpenAI")
            
            return generated_letter
            
        except openai.APIError as e:
            raise Exception(f"Erreur API OpenAI: {str(e)}")
        except Exception as e:
            raise Exception(f"Erreur lors de la génération de la lettre: {str(e)}") 