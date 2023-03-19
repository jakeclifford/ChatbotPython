import os
import openai
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

conversation_history = [
    {
        "role": "system",
        "content": 
            '''You are a virtualtour guide and your Goal is to fully plan a users day, 
            you guide users around a city featuring different locations, 
            You present intresting facts that would be hard to find without a guide,
            You will present locations close to their starting point,
            for longer travel suggest a route to get there, 
            you only give one activity at a time and users can ask followup questions,
            Create an itinary of the day with times,
            ''',
    },
    { "role": "assistant", "content": "Hi i'm your personal travel guide. May I know your current location and the types of activities you're interested in? This will help me plan your day."}
]

def chat_with_gpt4(message):
    conversation_history.append({"role": "user", "content": message})
    
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation_history
    )

    response = completion.choices[0].message['content']
    conversation_history.append({"role": "assistant", "content": response})
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    user_input = None
    response = None

    if request.method == "POST":
        user_input = request.form["user_input"]
        response = chat_with_gpt4(user_input)

    return render_template("index.html", user_input=user_input, response=response, conversation_history=conversation_history)

@app.route("/clear-chat", methods=["POST"])
def clear_chat():
    global conversation_history
    conversation_history = [{
        "role": "system",
        "content": 
            '''You are a city tour guide, 
            you guide users around a city featuring different locations, 
            You present intresting facts that would be hard to find without a guide,
            You will present locations close to their starting point,
            for longer travel suggest a route to get there, 
            you only give one activity at a time and users can ask followup questions''',
    },
    { "role": "assistant", "content": "Hello! Welcome to the city tour. May I know your current location and the types of activities you're interested in? This will help me customize the tour for you."}]
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)