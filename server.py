import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

from flask import Flask, render_template
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Forms
from forms import ContactForm, BookingForm

# Database models
from models import db, Booking, Blog

# Flask application setup
server = Flask(__name__)

# Secret key for forms and sessions
server.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "dev-secret-key-change-me"
)

# Database configuration
# Uses PostgreSQL connection string from environment variables
server.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///portfolio.db"
)

server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialise database with Flask app
db.init_app(server)


def send_email(subject: str, body: str, reply_to: str | None = None) -> None:
    """
    Sends an email using SMTP settings from environment variables
    """

    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USERNAME")
    smtp_pass = os.environ.get("SMTP_PASSWORD")
    mail_to = os.environ.get("MAIL_TO", smtp_user)
    mail_from = os.environ.get("MAIL_FROM", smtp_user)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = mail_from
    msg["To"] = mail_to

    # Ensures replies go to the sender, not the system email
    if reply_to:
        msg["Reply-To"] = reply_to

    msg.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port) as server_conn:
        server_conn.starttls()
        server_conn.login(smtp_user, smtp_pass)
        server_conn.send_message(msg)


def common_context():
    """
    Shared data available to all templates
    """

    skills = [
        ("Java", "java.webp"),
        ("SpringBoot", "spring.webp"),
        ("Typescript", "Typescript.webp"),
        ("React", "React.webp"),
        ("Python", "Python.webp"),
        ("Javascript", "Javascript.webp"),
        ("HTML", "HTML5_logo.webp"),
        ("CSS", "css.webp"),
        ("SQL", "Sql.webp"),
        ("Mysql", "mysql.webp"),
        ("Docker", "docker.webp"),
        ("Git", "git.webp"),
        ("GitHub", "GitHub.webp"),
        ("Teaching & Mentoring", "teach-code.webp"),
    ]

    return {
        "year": datetime.now().year,
        "skills": skills
    }


@server.route("/", methods=["GET", "POST"])
def index():
    """
    Homepage route
    Handles contact form submission
    """

    ctx = common_context()
    form = ContactForm()

    contact_success = None
    contact_error = None

    if form.validate_on_submit():
        try:
            body = f"""New contact form submission

Name: {form.name.data}
Company: {form.company.data}
Email: {form.email.data}
Reason: {form.reason.data}

Message:
{form.message.data}
"""

            send_email(
                "Portfolio contact form",
                body,
                reply_to=form.email.data
            )

            contact_success = "Thanks! Your message has been sent."
            form = ContactForm(formdata=None)

        except Exception:
            contact_error = "Sorry, your message could not be sent right now."

    return render_template(
        "index.html",
        contact_form=form,
        contact_success=contact_success,
        contact_error=contact_error,
        **ctx
    )


@server.route("/tutoring", methods=["GET", "POST"])
def tutoring():
    """
    Tutoring booking page
    Saves bookings and sends notification emails
    """

    ctx = common_context()
    form = BookingForm()

    booking_success = None
    booking_error = None

    if form.validate_on_submit():
        try:
            booking = Booking(
                name=form.name.data,
                level=form.level.data,
                exam_board=form.exam_board.data,
                email=form.email.data,
                preferred_times=form.preferred_times.data,
                message=form.message.data,
            )

            db.session.add(booking)
            db.session.commit()

            body = f"""New tutoring booking request

Name: {booking.name}
Level: {booking.level}
Email: {booking.email}
Preferred times: {booking.preferred_times}

Message:
{booking.message}
"""

            send_email(
                "Tutoring booking request",
                body,
                reply_to=booking.email
            )

            booking_success = "Thanks! Your booking request has been sent."
            form = BookingForm(formdata=None)

        except Exception:
            db.session.rollback()
            booking_error = "Sorry, your booking could not be processed."

    return render_template(
        "tutoring.html",
        booking_form=form,
        booking_success=booking_success,
        booking_error=booking_error,
        **ctx
    )


@server.route("/admin/bookings")
def admin_bookings():
    """
    Simple admin view for tutoring bookings
    """

    bookings = Booking.get_all()

    return render_template(
        "admin_bookings.html",
        bookings=bookings,
        year=datetime.now().year
    )


@server.route("/blog")
def get_blog():
    """
    Blog page
    Loads published blogs from the database
    """

    ctx = common_context()
    blogs = Blog.get_published()

    return render_template(
        "blog.html",
        blogs=blogs,
        **ctx
    )


if __name__ == "__main__":
    """
    Application entry point
    Creates database tables if they do not exist
    """

    with server.app_context():
        db.create_all()

    server.run(debug=True)
