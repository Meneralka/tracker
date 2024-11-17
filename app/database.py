from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password=password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Tasks(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column()
    name: so.Mapped[str] = so.mapped_column(sa.String(256))
    desc: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    section_url: so.Mapped[str] = so.mapped_column(sa.String(256))
    progress: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=0)

class Sections(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    section: so.Mapped[str] = so.mapped_column(sa.String(256))
    section_url: so.Mapped[str] = so.mapped_column(sa.String(256))
    user_id: so.Mapped[int] = so.mapped_column()


@login.user_loader
def load_user(id):
  return db.session.get(User, int(id))