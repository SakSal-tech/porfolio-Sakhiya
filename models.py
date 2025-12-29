# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# This db object is shared across the app
# (equivalent to EntityManagerFactory / SessionFactory)
db = SQLAlchemy()


class Booking(db.Model):
    """
    Booking model
    Equivalent to a JPA @Entity
    """

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), nullable=False)
    level = db.Column(db.String(20), nullable=False)
    exam_board = db.Column(db.String(60))
    email = db.Column(db.String(120), nullable=False)
    preferred_times = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="pending"
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    def __repr__(self):
        return (
            f"<Booking id={self.id} "
            f"email={self.email} "
            f"level={self.level} "
            f"status={self.status}>"
        )

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, booking_id: int):
        return cls.query.get(booking_id)

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_recent(cls, limit: int = 10):
        return (
            cls.query
            .order_by(cls.created_at.desc())
            .limit(limit)
            .all()
        )

    @classmethod
    def get_by_status(cls, status: str):
        return (
            cls.query
            .filter_by(status=status)
            .order_by(cls.created_at.desc())
            .all()
        )

    @classmethod
    def get_by_level(cls, level: str):
        return (
            cls.query
            .filter_by(level=level)
            .order_by(cls.created_at.desc())
            .all()
        )

    @classmethod
    def get_by_email(cls, email: str):
        return (
            cls.query
            .filter_by(email=email)
            .order_by(cls.created_at.desc())
            .all()
        )

    def mark_confirmed(self):
        self.status = "confirmed"
        db.session.commit()

    def mark_cancelled(self):
        self.status = "cancelled"
        db.session.commit()

    def is_alevel(self) -> bool:
        return self.level == "alevel"


class Blog(db.Model):
    """
    Blog model

    Represents one blog article displayed on the blog page.
    """

    __tablename__ = "blogs"

    id = db.Column(db.Integer, primary_key=True)

    slug = db.Column(db.String(100), unique=True, nullable=False)
    card_position = db.Column(db.Integer, nullable=False)

    title = db.Column(db.Text, nullable=False)
    meta = db.Column(db.Text)
    summary = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    read_time = db.Column(db.String)  # Added later

    published = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Blog id={self.id} slug={self.slug}>"

    @classmethod
    def get_published(cls):
        return (
            cls.query
            .filter_by(published=True)
            .order_by(cls.card_position)
            .all()
        )
