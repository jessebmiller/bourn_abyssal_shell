from flask import Flask, request, session, send_from_directory
import os
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")
openai.api_key = os.getenv('OPENAI_API_KEY')

missing_required_config = False
if openai.api_key is None or openai.api_key == "":
    print("OPENAI_API_KEY is not set")
    print("put OPENAI_API_KEY=<your key here> in src/.env")
    missing_required_config = True

if app.secret_key is None or app.secret_key == "":
    print("APP_SECRET_KEY is not set")
    print("put APP_SECRET_KEY=<random string> in src/.env")
    missing_required_config = True

if missing_required_config:
    exit(1)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css')

@app.route('/execute-command', methods=['POST'])
def execute_command():
    command = request.form.get('command')

    # Store the command in session history
    if 'history' not in session:
        session['history'] = []
    session['history'].append(command)
    session.modified = True  # Ensure the session gets saved

    # TODO: Interface with LLM and get a response.
    # For this example, we're just using a basic GPT-3 prompt.
    # You can expand this with more complex interactions.
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=f'''pretend I'm a linux terminal\n\n# {command}\n\n''',
      max_tokens=150
    ).choices[0].text.strip()

    print(session['history'])
    return f'<p class="response">{response}</p>'

if __name__ == '__main__':
    app.run(debug=True, port=8080)

