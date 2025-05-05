from flask import Blueprint, render_template, redirect, url_for
from app.models.product import KitType

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get kit types for the landing page
    kits = KitType.query.all()
    return render_template('index.html', kits=kits)

@main_bp.route('/features')
def features():
    return render_template('features.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')