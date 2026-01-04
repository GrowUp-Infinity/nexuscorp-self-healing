import json
import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def fix_security_issues():
    with open('trivy-report.json', 'r') as f:
        report = json.load(f)

    prompt = f"""
    Tu es un expert en cybersécurité. Voici un rapport de fautes Trivy :
    {json.dumps(report, indent=2)}
    
    Propose un nouveau fichier 'requirements.txt' qui corrige ces vulnérabilités.
    Réponds UNIQUEMENT avec les lignes du fichier, sans bloc de code markdown, sans texte.
    """

    print("🤖 NexusCorp AI analyse le rapport...")
    response = model.generate_content(prompt)
    
    # --- NETTOYAGE CRITIQUE ---
    # On enlève les backticks (```) et le mot "text" ou "requirements" si l'IA les ajoute
    content = response.text.replace("```", "").replace("text", "").replace("requirements.txt", "").strip()
    
    with open('requirements.txt', 'w') as f:
        f.write(content)
    
    print("✅ Le fichier requirements.txt a été réparé proprement.")

if __name__ == "__main__":
    fix_security_issues()