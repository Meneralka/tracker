from flask import redirect, render_template
from flask_login import current_user, login_required
import sqlalchemy as sa
from app.database import User, Sections
from app import db
from app import app


@app.route('/account', methods=['GET'])
@login_required
def profile():
    if not current_user.is_authenticated:
        return redirect('/login')
    user = db.session.scalar(
        sa.select(User).where(User.id == current_user.id)
    )
    sections = db.session.scalars(
        sa.select(Sections).where(Sections.user_id == current_user.id)
    ).all()
    user = {"username":user.username, 'email': user.email}
    return render_template('profile.html',
                           user=user, sections=sections)