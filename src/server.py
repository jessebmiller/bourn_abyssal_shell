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

def make_prompt(history):
    """ Create a prompt from the history of messages """
    prompt = "The following is a conversation with an AI acting as a mystery game for a human. The AI is responding with only the text that a debian linux terminal would output. "
    prompt += "The twist is that a cosmic horror old god has possessed the machine and is trying to gently coax the human into starting a cult in their name. "
    prompt += "The human is here to have fun exploring this weird system and is to understand and explore what's going on. "
    prompt += "\n\n"
    prompt += "\n".join(history[-10:])
    prompt += "\n"
    print(prompt)
    return prompt

@app.route('/execute-command', methods=['POST'])
def execute_command():
    command = request.form.get('command')

    # Store the command in session history
    if 'history' not in session:
        session['history'] = []

    session['history'].append("$ " + command)

    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=make_prompt(session['history']),
      max_tokens=150
    ).choices[0].text.strip()

    session['history'].append(response)
    session.modified = True  # Ensure the session gets saved

    return "<p>$ " + command + "</p>" + ''.join([f'<p class="response">{r}</p>' for r in response.split('\n')])

if __name__ == '__main__':
    app.run(debug=True, port=8880)

