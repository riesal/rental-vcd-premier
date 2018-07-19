import os, json
from flask import Flask, make_response
from werkzeug.exceptions import NotFound

# addon
def root_dir():
    """ Returns root director for this project """
    #return os.path.dirname(os.path.realpath(__file__ + '/..'))
    return os.path.dirname(os.path.realpath(__file__ + '/'))

def nice_json(arg):
    response = make_response(json.dumps(arg, sort_keys = True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response
# end-addon

app = Flask(__name__)

with open("{}/premier.json".format(root_dir()), "r") as f:
    showtimes = json.load(f)


@app.route("/", methods=['GET'])
def hello():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "showtimes": "/showtimes",
            "showtime": "/showtimes/<date>"
        }
    })


@app.route("/showtimes", methods=['GET'])
def showtimes_list():
    return nice_json(showtimes)


@app.route("/showtimes/<date>", methods=['GET'])
def showtimes_record(date):
    if date not in showtimes:
        raise NotFound
    print showtimes[date]
    return nice_json(showtimes[date])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=6002, use_reloader=True)
