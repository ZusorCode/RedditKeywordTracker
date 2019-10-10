from flask import Flask, render_template, jsonify
import redis
import config
import pickle
config_data = config.Config()

app = Flask(__name__)


db = redis.Redis(host=config_data.redis_host, port=6379, db=0)


def get_titles():
    if db.get("enabled"):
        keys = sorted(db.keys())
        key_name = keys[len(keys)-1]
        return pickle.loads(db.get(key_name))


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/api/<string:keyword>")
def api(keyword):
    counter = 0
    titles = get_titles()
    if titles:
        for post in titles:
            if keyword.lower() in post.lower():
                counter += 1
        return jsonify({"count": counter})
    else:
        return jsonify({"count": 0})


if __name__ == '__main__':
    app.run()
