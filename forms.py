from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=80)])
    company = StringField("Company", validators=[Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    reason = SelectField(
        "Reason for Contact",
        choices=[
            ("recruiter", "Recruiter"),
            ("team_lead", "Team Lead"),
            ("backend_java", "Backend Developer"),
            ("fullstack", "Full-Stack Engineer"),
            ("junior_engineer", "Junior Software Engineer"),
            ("freelance", "Freelance / Client Project"),
            ("collaboration", "Collaboration / Networking"),
            ("other", "Other"),
        ],
        validators=[DataRequired()],
    )
    message = TextAreaField("Message", validators=[DataRequired(), Length(max=2000)])


class BookingForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=80)])
    level = SelectField(
        "Level",
        choices=[("gcse", "GCSE"), ("alevel", "A-Level")],
        validators=[DataRequired()],
    )
    exam_board = StringField("Exam board", validators=[Length(max=60)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    preferred_times = StringField("Preferred days/times", validators=[Length(max=200)])
    message = TextAreaField("Topics / message", validators=[DataRequired(), Length(max=2000)])




class ReviewForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired(), Length(max=80)]
    )

    reviewer_type = SelectField(
        "Reviewer type",
        choices=[
            ("parent", "Parent"),
            ("student", "Student"),
            ("colleague", "Colleague / Professional"),
        ],
        validators=[DataRequired()]
    )

    role = StringField(
        "Role / Position (optional)",
        validators=[Length(max=120)]
    )

    message = TextAreaField(
        "Review",
        validators=[DataRequired(), Length(min=20)]
    )
    submit = SubmitField("Submit review")

