from flask import Flask,request,redirect,jsonify,render_template,abort,url_for
from db import db
from models import URL,Visit
from utils import generate_short_code
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shortener.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
  db.create_all()

@app.route("/",methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/shorten",methods=["POST"])
def shorten():
    data = request.get_json(silent=True) or request.form
    original_url = data.get("url")
    custom_alias = data.get("custom_alias")

    if not original_url:
        return jsonify({"error":"URL required"}),400
    
    code = custom_alias if custom_alias else generate_short_code()

    url = URL(original_url = original_url,short_code = code)
    try:
        db.session.add(url)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error":"Alias already exists"}),409
    
    short_url = request.host_url+code
    if request.is_json:
        return jsonify({"short_url":short_url,"original_url":original_url})
    return render_template("index.html",short_url=short_url)

@app.route("/<code>")
def redirect_to_url(code):
    url = URL.query.filter_by(short_code = code).first()
    if not url:
        abort(404)
    visit = Visit(url_id=url.id,user_agent = request.headers.get("User-Agent"),referrer=request.referrer)
    db.session.add(visit)
    db.session.commit()

    return redirect(url.original_url,code=302)

@app.route("/info/<code>")
def info(code):
    url = URL.query.filter_by(short_code = code).first()
    if not url:
        return jsonify({"error":"Not found"}),404
    return jsonify({
        "original_url":url.original_url,
        "short_code":url.short_code,
        "created_at":url.created_at.isoformat(),
        "visits":len(url.visits)
    })

if __name__ == "__main__":
    app.run(debug=True)
