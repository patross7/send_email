from flask import Flask, render_template, request
from flask_mail import Mail, Message
import requests
from datetime import datetime

now = datetime.now()
now = now.strftime("%Y-%m") 

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'your_mail@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send_email", methods=["POST"])
def send_email():
    email = request.form.get("email")
    topic = request.form.get("topic")
    
    news_response = requests.get("https://newsapi.org/v2/everything?" \
                                    f"q={topic}&" \
                                    f"from={now}" \
                                    "-04&sortBy=publishedAt&" \
                                    "apiKey=3b8626bca942449dba38ad9b7b63247b&" \
                                    "language=pl")
    news_data = news_response.json()
    
    if news_data['totalResults'] == 0:
        return f"No news found for the topic '{topic}'."
    
    msg = Message(f"Email with your news about {topic}",
                    sender="your_email@gmail.com",
                    recipients=[email])
    
    msg.body = ""
    for article in news_data['articles'][:20]:
        if article['title'] and article['description'] is not None:
            msg.body += article["title"] + "\n" \
                        + article["description"] \
                        + "\n" + article["url"] + 2*"\n"

    msg.body = msg.body.encode("utf-8")
    mail.send(msg)
    return "Email sent successfully to " + email


if __name__ == "__main__":
    app.run(debug=True)


