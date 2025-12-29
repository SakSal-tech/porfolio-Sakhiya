import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

import smtplib
from email.message import EmailMessage
from datetime import datetime
from flask import Flask, render_template
from flask import flash, redirect, url_for


# Forms
from forms import ContactForm, BookingForm

# Database models
from models import db, Booking, Blog

# Flask application
server = Flask(__name__)


# Secret key for forms and sessions
server.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "dev-secret-key-change-me"
)



# Database configuration
# Uses DATABASE_URL if explicitly set, otherwise falls back to SQLite
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
server.config["SQLALCHEMY_DATABASE_URI"] = (
    os.environ.get("DATABASE_URL")
    or f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'portfolio.db')}"
)

# It disables SQLAlchemy’s event-based object change tracking, which it is not used it now.
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
print("USING DB:", server.config["SQLALCHEMY_DATABASE_URI"])

# Initialise database with Flask app
db.init_app(server)

# Had issues with blog table not existing when updating blog as it is dropped. Only creates missing ones
with server.app_context():
    db.create_all()


# Reads SMTP config from environment.
# Constructs an email and sends it securely.
def send_email(subject, body, reply_to=None):
    """
    Sends an email using SMTP settings from environment variables
    """
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USERNAME")
    smtp_pass = os.environ.get("SMTP_PASSWORD")
    mail_to = os.environ.get("MAIL_TO", smtp_user)
    mail_from = os.environ.get("MAIL_FROM", smtp_user)

    # Fail early with a clear error if config is missing
    if not all([smtp_host, smtp_port, smtp_user, smtp_pass]):
        raise RuntimeError("SMTP environment variables are not fully configured")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = mail_from
    msg["To"] = mail_to

    if reply_to:
        msg["Reply-To"] = reply_to

    msg.set_content(body)

    # SAFE SMTP FLOW (prevents 'please run connect() first')
    with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server_conn:
        server_conn.ehlo()

        # STARTTLS is only valid on TLS ports (usually 587)
        if smtp_port == 587:
            server_conn.starttls()  # Upgrades the connection to encrypted TLS
            server_conn.ehlo()

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
        "skills": skills,
    }


@server.route("/", methods=["GET", "POST"])
def index():
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
                subject="Portfolio contact form",
                body=body,
                reply_to=form.email.data
            )

            # Redirect after successful POST (PRG pattern)
            flash("Thanks! Your message has been sent. I will get back to you", "success")
            return redirect(url_for("index", _anchor="contact-form"))

        except Exception:
            server.logger.exception("Contact form email failed")
            flash("Sorry, your message could not be sent right now.", "error")
            return redirect(url_for("index", _anchor="contact-form"))


    return render_template(
        "index.html",
        contact_form=form,
        contact_success=contact_success,
        contact_error=contact_error,
        **ctx
    )



@server.route("/tutoring", methods=["GET", "POST"])
def tutoring():
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
                subject="Tutoring booking request",
                body=body,
                reply_to=booking.email
            )

            # Redirect to the form after submission so user can see message instead of scrolling it up.
            flash("Thanks! Your booking request has been sent.", "success")
            return redirect(url_for("tutoring", _anchor="booking-form"))


        except Exception:
            db.session.rollback()
            server.logger.exception("Tutoring booking failed")
            flash("Sorry, your booking could not be processed.", "error")
            return redirect(url_for("tutoring", _anchor="booking-form"))


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
