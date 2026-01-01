from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db
from .models import User, Gift, Friend, FriendRequest
from .forms import FindFriendForm


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/friends', methods=['GET', 'POST'])
@login_required
def friends():
    # Friends tab
    friend_ids = db.session.execute(db.select(Friend).filter_by(uid1=current_user.id)).scalars()
    friends = [db.session.execute(db.select(User).filter_by(id=friend_id)).scalar_one_or_none() for friend_id in friend_ids]

    # Pendings
    incoming_request_ids = db.session.execute(db.select(FriendRequest).filter_by(user_id=current_user.id))
    incoming_requests = [db.session.execute(db.select(User).filter_by(id=incoming_request_id)).scalar_one_or_none() for incoming_request_id in incoming_request_ids]
    outgoing_request_ids = db.session.execute(db.select(FriendRequest).filter_by(friend_id=current_user.id))
    outgoing_requests = [db.session.execute(db.select(User).filter_by(id=outgoing_request_id)).scalar_one_or_none() for outgoing_request_id in outgoing_request_ids]


    # Find friend
    active_tab = None
    found_friend = None
    if request.method == 'POST':
        print('here')
        active_tab = 'request-tab'
        friend_email = request.form.get('email')
        found_friend = db.session.execute(db.select(User).filter_by(email=friend_email)).scalar_one_or_none()
        if not found_friend:
            flash(f'User {friend_email} not found. No fuzzy searches as of now. Must be char for char how they entered it :(')

    return render_template(
        'friends.html',
        friends=friends,
        incoming_requests=incoming_requests,
        outgoing_requests=outgoing_requests,
        found_friend=found_friend,
        active_tab=active_tab
    )




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

