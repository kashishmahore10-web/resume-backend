from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    try:
        import groq
        client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))
        data = request.json
        user_info = data.get('userInfo', '')
        job_description = data.get('jobDescription', '')

        prompt = f"""
        Create a professional resume based on:
        User Information: {user_info}
        Job Description: {job_description}
        Generate a complete ATS-friendly resume with Summary, Experience, Skills, Education.
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
        import groq
        client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))
        data = request.json
        resume_text = data.get('resume', '')
        job_description = data.get('jobDescription', '')

        prompt = f"""
        Improve this resume to better match the job description:
        Current Resume: {resume_text}
        Job Description: {job_description}
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
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)