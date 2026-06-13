from flask import Flask, request, jsonify
from flask_cors import CORS
import groq
import os

app = Flask(__name__)
CORS(app)

# Initialize Groq client
client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    try:
        data = request.json
        user_info = data.get('userInfo', '')
        job_description = data.get('jobDescription', '')

        prompt = f"""
        Create a professional resume based on the following information:
        
        User Information:
        {user_info}
        
        Job Description they are applying for:
        {job_description}
        
        Generate a complete, ATS-friendly resume with:
        - Professional Summary
        - Work Experience
        - Skills
        - Education
        Format it cleanly and professionally.
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )

        resume = chat_completion.choices[0].message.content
        return jsonify({"resume": resume, "status": "success"})

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/improve-resume', methods=['POST'])
def improve_resume():
    try:
        data = request.json
        resume_text = data.get('resume', '')
        job_description = data.get('jobDescription', '')

        prompt = f"""
        Improve this resume to better match the job description:
        
        Current Resume:
        {resume_text}
        
        Job Description:
        {job_description}
        
        Provide an improved version with better keywords and formatting.
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )

        improved = chat_completion.choices[0].message.content
        return jsonify({"resume": improved, "status": "success"})

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)