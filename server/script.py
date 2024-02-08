import logging
from flask import Flask, request, jsonify
from PIL import Image
from flask_cors import CORS
import cv2
from PIL import Image, ImageEnhance
import numpy as np
import pytesseract as tess
import openai
import re
import os
from dotenv import load_dotenv


# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Configuration des journaux
logging.basicConfig(level=logging.DEBUG)

# Récupérer la clé API à partir des variables d'environnement
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)
@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        logging.info('Requête reçue sur /process_image')
        file = request.files['file']
        typ = request.form.get('type')
        logging.info('Nom du fichier reçu : %s', file.filename)

        processed_text = process_image_logic(file, typ)
        logging.info('Réponse générée avec succès : %s', processed_text)

        return jsonify({'processed_text': processed_text})
    except Exception as e:
        logging.error('Erreur lors du traitement de l\'image : %s', str(e))
        return jsonify({'error': str(e)})

def get_answer(image_file, question):
    original_image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Appliquer des transformations
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    pil_image = Image.fromarray(gray_image)
    enhancer = ImageEnhance.Contrast(pil_image)
    enhanced_image = enhancer.enhance(3.0)  # Ajustez le facteur de contraste selon vos besoins.

    # Utiliser Tesseract pour récupérer le texte
    text = tess.image_to_string(enhanced_image)
    question = question + text
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  # Choisissez le moteur en fonction de vos besoins
        prompt=question,
        max_tokens=200,  # Limite le nombre de tokens dans la réponse
    )
    answer = response.choices[0].text.strip()
    answer = re.sub(r'\n+', '\n', answer)
    return answer

def get_question(typ):
    if (typ == 'text'):
        return "You are a very experienced English teacher. I give you a text with THREE questions and 4 choices for each question. Analyze the text and give me the answer for each questions.\n"
    elif (typ == 'hole'):
        return "You are a very experienced English teacher. I'll give you a blank text. Analyze the text and give me the answer for the hole. I want a certain format for your answer, I want you to answer the correct answer and after returning to the line you explain to me effectively why it is the correct answer\n"
    return None

def process_image_logic(file, typ):
    question = get_question(typ)
    if (question != None):
        answer = get_answer(file, question)
        return answer
    return None

if __name__ == '__main__':
    app.run(debug=True, port=5000)