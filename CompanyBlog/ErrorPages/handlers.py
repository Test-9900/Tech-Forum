from flask import Blueprint,render_template,flash

errorPages = Blueprint('errorPages',__name__)

@errorPages.app_errorhandler(404)
def error404(error):
    return render_template('errorPages/404.html'),404

@errorPages.app_errorhandler(403)
def error403(error):
    return render_template('errorPages/403.html'),403

@errorPages.app_errorhandler(500)
def error403(error):
    flash('Password does not match!')
    return render_template('login.html'),500
