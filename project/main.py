from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db
from .models import User, Gift, Friend, FriendRequest


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.post('/send_request')
@login_required
def send_request():
    friend_id = request.form.get('friend_id')
    friend_request = FriendRequest(
        requestor_id=current_user.id,
        requestee_id=friend_id,
    )
    db.session.add(friend_request)
    db.session.commit()
    return render_template('send_request.html')



@main.route('/friends', methods=['GET', 'POST'])
@login_required
def friends():
    # Friends tab
    friend_ids = db.session.execute(db.select(Friend).filter_by(user_id=current_user.id)).scalars()
    friends = [db.session.execute(db.select(User).filter_by(id=friend_id)).scalar_one_or_none() for friend_id in friend_ids]

    # Pendings
    requestor_ids = [r.requestor_id for r in db.session.execute(db.select(FriendRequest).filter_by(requestee_id=current_user.id)).scalars()]
    requestors = [db.session.execute(db.select(User).filter_by(id=requestor_id)).scalar_one_or_none() for requestor_id in requestor_ids]
    requestee_ids = [r.requestee_id for r in db.session.execute(db.select(FriendRequest).filter_by(requestee_id=current_user.id)).scalars()]
    requestees = [db.session.execute(db.select(User).filter_by(id=requestee_id)).scalar_one_or_none() for requestee_id in requestee_ids]
    print(requestors)
    print(requestees)

    # Find friend
    active_tab = None
    found_friend = None
    if request.method == 'POST':
        active_tab = 'request-tab'
        friend_email = request.form.get('email')
        found_friend = db.session.execute(db.select(User).filter_by(email=friend_email)).scalar_one_or_none()
        if not found_friend:
            flash(f'User {friend_email} not found. No fuzzy searches as of now. Must be char for char how they entered it :(')
        if found_friend.id == current_user.id:
            found_friend = None
            flash(f'That\'s you. Pick someone else.')

    return render_template(
        'friends.html',
        friends=friends,
        incoming_requests=requestors,
        # outgoing_requests=requestees,
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

