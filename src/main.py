from flask import Flask, render_template, request, jsonify
import ollama
import asyncio
import markdown

app = Flask(__name__)


async def get_chatbot_response(user_query):
    try:
        response = await asyncio.to_thread(ollama.chat, model='V:latest', messages=[
            {
                'role': 'user',
                'content': user_query
            }
        ])

        full_response = response.get('message', {}).get('content', '')
        return full_response if full_response else "Ollama response was empty."

    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/chat', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_query = request.form['query']

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        bot_markdown_response = loop.run_until_complete(
            get_chatbot_response(user_query))
        bot_html_response = markdown.markdown(bot_markdown_response)

        return jsonify({"response": bot_html_response})

    return render_template('chat.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
