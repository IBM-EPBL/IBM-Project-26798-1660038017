from mailjet_rest import Client
from flask import current_app, g


def send_email_alert():

    mail_api_key = current_app.config['MAIL_API_KEY']
    mail_api_secret = current_app.config['MAIL_API_SECRET']
    mail_admin = current_app.config['ADMIN_MAIL']
    mailjet = Client(auth=(mail_api_key, mail_api_secret), version='v3.1')
    name = g.user["NAME"]
    email = g.user["EMAIL"]
    data = {
        'Messages': [
            {
                "From": {
                    "Email": mail_admin,
                    "Name": "Admin"
                },
                "To": [
                    {
                        "Email": email,
                        "Name": name
                    }
                ],
                "Subject": "Expense Alert",
                "HTMLPart": f"<h3>Dear {name},<br/> your expenses have crossed the monthly expense limit set by you.",
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result)
