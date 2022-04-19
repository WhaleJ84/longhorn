"""
Contains all the functions needed for the email blueprint.
Things such as routes and forms should be in separate files.
"""
from flask import current_app as app
from flask import g
from flask_mail import Mail, Message

mail = Mail()


def send_email(email: Message):
    """
    Sends the given email, with the sender and recipient defined by the Message itself.

    Returns a dictionary containing the following:

    - subject
    - recipients
    - message
    - sender
    - cc
    - outbox

    :param email: The Message object containing all email details
    """
    try:
        with mail.record_messages() as outbox:
            mail.send(email)

        response = dict(
            {
                "subject": email.subject,
                "recipients": email.recipients,
                "message": email.body,
                "sender": email.sender,
                "cc": email.cc,
                "outbox": len(outbox),
            }
        )

        return response
    except ConnectionRefusedError:
        app.logger.error(f"{g.process_id}\tFailed to send email: {email.body}")
        return None


def send_alert_transport_via_email(response: dict):
    """
    Sends an email to app.config["ENGINEERS_EMAIL"] with the response
    details using app.config["MAIL_DEFAULT_SENDER"] as sender.

    Returns a dictionary containing the following:

    - subject
    - recipients
    - message
    - sender
    - cc
    - outbox

    :param response: The response object returned from Flask
    """
    email = Message(
        subject=f"{g.process_id}: {response['message']}",
        recipients=[app.config["ENGINEERS_EMAIL"]],
        body=f"The following information has been gathered for {g.process_id}:\n{response}",
    )
    app.logger.info(f"{g.process_id}\tsent message: {email.body} to: {email.recipients}")

    return send_email(email)
