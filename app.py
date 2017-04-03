import os
from datetime import *
from flask import *
from flask_login import *
from werkzeug.utils import *

import mlab
from  models.fooditem import FoodItem
from models.sessionuser import *
from models.user import *

app = Flask(__name__)

mlab.connect()
## create forder uploads
app.config["UPLOAD_PATH"] =  os.path.join(app.root_path, "uploads")
if not os.path.exists(app.config["UPLOAD_PATH"]):
    os.makedirs(app.config["UPLOAD_PATH"])

app.secret_key = "himistu"

login_manager = LoginManager()
login_manager.init_app(app)

# admin_user = User()
# admin_user.username = "admin"
# admin_user.password = "admin"
# admin_user.save()

@login_manager.user_loader
def user_loader(user_token):
    found_user = User.objects(token= user_token).first()
    if found_user:
        session_user =  SessionUser(found_user.id)
        return session_user


@app.route('/login2' , methods= [ "GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login2.html")
    elif request.method == "POST":
        user = User.objects(username=request.form ["username"]).first()
        if user and user.password == request.form["password"]:
            session_user = SessionUser(user.id)
            user.update(set__token = str(user.id))
            login_user (session_user)
            return redirect(url_for("add_food"))
        else:
            return redirect(url_for("login2.html"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/')
def hello_world():
    return redirect(url_for("login"))
number_visitor = 0

image_list = [
    { "src" : "https://i.ytimg.com/vi/icSRtb0Vbcs/maxresdefault.jpg",
      "title" : " abc",
      "tag" : " abc"
      },
    { "src" : "https://s-media-cache-ak0.pinimg.com/originals/f9/d1/74/f9d17484e7445115a4e0360332147577.jpg",
      "title": "acb",
      "tag" : " acb"
      },
    { "src" : "http://tghinhanhdep.com/wp-content/uploads/2015/10/tai-hinh-nen-tinh-yeu-doi-lua-dep-nhat-11.jpg",
    "title" : " acb",
    "tag" : "acb",
      }
             ]
#


@app.route("/addfood",methods=["GET", "POST"])
@login_required

def add_food():
    if request.method == "GET":
        return render_template("addfood.html")
    if request.method == "POST":
        file = request.files["source"]
        if file:
            filename = secure_filename(file.filename)

        if os.path.join(app.config["UPLOAD_PATH"], filename):
            name_index = 0
            original_name = filename.rsplit(".",1) [0]
            original_extension = filename.rsplit("1",1) [1]
            while os.path.exists(os.path.join(app.config["UPLOAD_PATH"], filename)):
                name_index += 1
                filename = "{0} ({1}).(2)".format(original_name, name_index, original_extension)

        file.save(os.path.join(app.config["UPLOAD_PATH"], filename))

        new_food = FoodItem()
        new_food.src = url_for("uploads_file", filename = filename)
        new_food.title = request.form["title"]
        new_food.description = request.form["description"]
        new_food.save()
        return render_template("addfood.html")

@app.route("/uploads/<filename>")
def uploads_file(filename):
    return send_from_directory(app.config["UPLOAD_PATH"], filename)


@app.route("/deletefood", methods=["GET", "POST"])
def delete_food():
    if request.method == "GET":
        return render_template("deletefood.html")
    if request.method == "POST":
        new_food = FoodItem.objects(title =request.form["title"]).first()
        if new_food is not None:
            new_food.delete()
        return render_template("deletefood.html")

@app.route("/editfood", methods=["GET", "POST"])
def edit_food():
    if request.method == "GET":
        return render_template("editfood.html")
    if request.method == "POST":
        edit_food = FoodItem.objects(title = request.form["title"]).first()
        if edit_food is not None:
            edit_food.src = request.form["source"]
            edit_food.title = request.form["title"]
            edit_food.description = request.form["description"]
            edit_food.save()
        return render_template("editfood.html")

# @app.route("/login")
# def login():
#     global number_visitor
#     number_visitor += 1
#     current_time_sever = str(datetime.now())
#     return render_template("login.html", )
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/food")
def food():
    return render_template("food.html", image_list=image_list)

@app.route("/foodblog")
def foodblog():
    return render_template("foodblog.html", food_list = FoodItem.objects())

if __name__ == '__main__':
    app.run()