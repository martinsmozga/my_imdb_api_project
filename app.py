
# part1 
# Route the CSV
# route Get on/

from flask import Flask, request
import json
from my_csv_parser import movie_filter

app= Flask(__name__)

@app.route('/') 
def root():
    genre = request.args.get("genre", "").strip()
    my_list = movie_filter(genre)
    return json.dumps(my_list)
    # return Response(json.dumps(data), mimetype="application/json") // best practice, as then Flask knows it Json

@app.route('/<genre_name>')
def by_path(genre_name):
    # These next two lines are relevant if testing in a reaol browser not in the IDE.
    # if genre_name.lower() == "favicon.ico":
    #     return Response("[]", mimetype="application/json")
    print(request.args.get("genre"))
    data = movie_filter(genre_name)
    return json.dumps(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)