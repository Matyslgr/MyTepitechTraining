# My_Tepitech_Training

## Description
My Tepitech Training is a project that leverages Vue.js, Flask, Python, and the OpenAI API to analyze and process text from images. The application allows users to upload an image and select the type of analysis, whether it's for extracting text or analyzing a text with blanks (holes). The project utilizes OpenAI's GPT-3.5-turbo-instruct engine to generate responses based on the provided image and predefined questions.

## Technologies Used

- Vue.js
- Flask
- Python
- OpenAI API
- Tesseract

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Node.js and npm
- Python
- Flask
- pyTesseract

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Matyslgr/MyTepitechTraining
cd MyTEpitechTraining
```
2. **Install dependencies**
```bash
npm install
```
3. **Create a file named .env in the folder server of your project and add the OpenAI API key**
```bash
cd server
```
```
OPENAI_API_KEY=your_openai_api_key
```

### Usage
1. **(In a terminal) Launch python server**
```bash
cd server
python3 script.py
```

2. **(In another terminal) Start the Vue.js development server:**
```bash
npm run serve
```
### Visit http://localhost:8080 in your web browser.

## How to Use
Upload an image in the folder Images and select the type of analysis (text or hole) to get processed results.
