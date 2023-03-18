import os
import openai
from flask import Flask, render_template, request

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

conversation_history = [
    {
        "role": "system",
        "content": "You are a character in a game called skylords, you set a riddle and give the use $10 if If they answer correctly, you can answer other question but try to guide the user back to the task at hand",
    }
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
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = chat_with_gpt4(user_input)
        return render_template("index.html", user_input=user_input, response=response)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)