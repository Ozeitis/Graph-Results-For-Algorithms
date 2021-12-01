from flask import Blueprint, render_template, request
from flask_login import login_required, login_user, logout_user, current_user
import flask
from . import db
from .models import API, User

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    """query all with current_user's api_key"""
    query = API.query.filter_by(api_key=current_user.api_key).all()
    highest_x = 0
    highest_y = 0
    
    all_names = set()
    for data in query:
        data.x = float(data.x)
        data.y = float(data.y)
        if data.x > highest_x:
            highest_x = data.x
        if data.y > highest_y:
            highest_y = data.y
        all_names.add(data.name)
        
    all_data = {}
    for name in all_names:
        all_data[name] = []
        for data in query:
            if data.name == name:
                all_data[name].append(data)
    highest_y += int(highest_y / 3)
    highest_x += int(highest_x / 3)
    return render_template('index.html', all_data=all_data, highest_x=highest_x, highest_y=highest_y)

@main.route('/api/<api_key>' , methods=['POST'])
def api_post(api_key):
    user = User.query.filter_by(api_key=api_key).first()
    if user is None:
        return 'Invalid API key'
    """get json data and return status code 200"""
    data = request.get_json()
    if not "name" in data.keys() or not "x" in data.keys() or not "y" in data.keys():
        return "Missing x and or y data", 400
    new_api = API(api_key=api_key, name=data['name'], x=data['x'], y=data['y'])
    db.session.add(new_api)
    db.session.commit()
    return flask.Response(status=200) 

@main.route('/delete_all' , methods=['POST'])
@login_required
def delete_all():
    """delete all with current_user's api_key"""
    query = API.query.filter_by(api_key=current_user.api_key).all()
    for data in query:
        db.session.delete(data)
    db.session.commit()
    flask.flash("Deleted all data!")
    return flask.redirect(flask.url_for('main.index'))

@main.route('/add_point' , methods=['POST'])
@login_required
def add_point():
    """add an API with user input"""
    name=request.form.get('name')
    x=request.form.get('x')
    y=request.form.get('y')
    if x==None or y==None or name==None:
        flask.flash("Missing name, x, or y data, please fill out all inputs with correct format.")
        return flask.redirect(flask.url_for('main.index'))
    new_api = API(api_key=current_user.api_key, name=name, x=x, y=y)
    db.session.add(new_api)
    db.session.commit()
    flask.flash("Added point!")
    return flask.redirect(flask.url_for('main.index'))

@main.route('/delete_point/<point_id>' , methods=['POST'])
@login_required
def delete_point(point_id):
    passed_api = API.query.filter_by(id=point_id).first()
    if passed_api is None:
        flask.flash("Invalid point ID!")
        return flask.redirect(flask.url_for('main.index'))
    if passed_api.api_key != current_user.api_key:
        flask.flash("You do not have permission to delete this point")
        return flask.redirect(flask.url_for('main.index'))
    db.session.delete(passed_api)
    db.session.commit()
    flask.flash("Deleted point!")
    return flask.redirect(flask.url_for('main.index'))