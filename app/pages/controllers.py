from flask import Blueprint
from flask import render_template
from flask_login import current_user
from flask_login import login_required

page = Blueprint("page", __name__)


@page.route("/profile")
@login_required
def profile():
    return render_template("page/profile.html", name=current_user.name)
