from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/api/ai/generate-resume', methods=['POST'])
def generate_resume():
    try:
        import groq
        client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))
        data = request.json
        prompt = f"""
        Create a professional resume based on:
        {data}
        Generate a complete ATS-friendly resume with Summary, Experience, Skills, Education.
        """
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        return jsonify({"result": chat_completion.choices[0].message.content, "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/improve-section', methods=['POST'])
def improve_section():
    try:
        import groq
        client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))
        data = request.json
        text = data.get('text', '')
        type_ = data.get('type', '')
        prompt = f"Improve this {type_} section for a resume:\n{text}"
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        return jsonify({"result": chat_completion.choices[0].message.content, "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/ats-score', methods=['POST'])
def ats_score():
    try:
        import groq
        client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))
        data = request.json
        resume_text = data.get('resumeText', '')
        job_description = data.get('jobDescription', '')
        prompt = f"""
        Analyze this resume against the job description and provide an ATS score out of 100.
        Resume: {resume_text}
        Job Description: {job_description}
        Provide score and detailed feedback in JSON format:
        {{"score": 85, "feedback": "...", "missing_keywords": [], "suggestions": []}}
        """
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        return jsonify({"result": chat_completion.choices[0].message.content, "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/improvement-suggestions', methods=['POST'])
def improvement_suggestions():
    try:
        import groq
        client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))
        data = request.json
        resume_text = data.get('resumeText', '')
        job_description = data.get('jobDescription', '')
        prompt = f"""
        Provide detailed improvement suggestions for this resume:
        Resume: {resume_text}
        Job Description: {job_description}
        Give specific actionable suggestions.
        """
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        return jsonify({"result": chat_completion.choices[0].message.content, "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/mock-interview/questions', methods=['POST'])
def interview_questions():
    try:
        import groq
        client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))
        data = request.json
        target_role = data.get('targetRole', '')
        experience_level = data.get('experienceLevel', '')
        num_questions = data.get('numQuestions', 5)
        prompt = f"""
        Generate {num_questions} interview questions for:
        Role: {target_role}
        Experience Level: {experience_level}
        Return as JSON array: [{{"id": 1, "question": "...", "category": "..."}}]
        """
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        return jsonify({"result": chat_completion.choices[0].message.content, "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/mock-interview/evaluate', methods=['POST'])
def evaluate_answer():
    try:
        import groq
        client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))
        data = request.json
        question = data.get('question', '')
        answer = data.get('answer', '')
        target_role = data.get('targetRole', '')
        prompt = f"""
        Evaluate this interview answer for {target_role}:
        Question: {question}
        Answer: {answer}
        Provide score out of 10 and detailed feedback in JSON:
        {{"score": 8, "feedback": "...", "improvements": []}}
        """
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        return jsonify({"result": chat_completion.choices[0].message.content, "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)