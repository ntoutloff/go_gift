from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from . import db
from .models import User, Gift

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/add_gift', methods=['GET', 'POST'])
@login_required
def add_gift():
    if request.method == 'POST':
        print(request.form)
        new_gift = Gift(
            gifter = current_user.id,
            giftee = int(request.form.get('giftee')),
            gift = request.form.get('gift'),
            details = request.form.get('details'),
            price = int(request.form.get('price')),
            link = request.form.get('link'),
        )
        db.session.add(new_gift)
        db.session.commit()
        return render_template('add_gift_success.html')
    
    # TODO: only return friends, not everyone in the db
    users = db.session.execute(db.select(User).order_by(User.name)).scalars()
    
    return render_template('add_gift.html', self_id=current_user.id, users=users)

