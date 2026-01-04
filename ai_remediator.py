import json
import os
import google.generativeai as genai

# Configuration de l'IA
# Si tu n'utilises pas de secret, remplace os.getenv par "TA_CLE_ICI" (déconseillé)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def fix_security_issues():
    # 1. Lire le rapport de fautes
    with open('trivy-report.json', 'r') as f:
        report = json.load(f)

    # 2. Préparer le message pour Gemini
    # On lui donne le JSON et on lui demande de corriger requirements.txt
    prompt = f"""
    Tu es un expert en cybersécurité. Voici un rapport de fautes Trivy :
    {json.dumps(report, indent=2)}
    
    Propose un nouveau fichier 'requirements.txt' qui corrige ces vulnérabilités 
    en mettant à jour les paquets (Werkzeug, Flask, etc.) vers leurs versions stables et sécurisées.
    Réponds UNIQUEMENT avec le contenu du fichier requirements.txt, rien d'autre.
    """

    # 3. Demander à l'IA de générer le correctif
    print("🤖 NexusCorp AI analyse le rapport...")
    response = model.generate_content(prompt)
    
    # 4. Écrire le nouveau fichier
    with open('requirements.txt', 'w') as f:
        f.write(response.text.strip())
    
    print("✅ Le fichier requirements.txt a été réparé par l'IA.")

if __name__ == "__main__":
    fix_security_issues()