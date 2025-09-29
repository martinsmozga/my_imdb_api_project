
# # part1 
# # Route the CSV
# # route Get on/

# from flask import Flask, request
# import json
# from my_csv_parser import movie_filter

# app= Flask(__name__)

# @app.route('/') 
# def root():
#     genre = request.args.get("genre", "").strip()
#     my_list = movie_filter(genre)
#     return json.dumps(my_list)
#     # return Response(json.dumps(data), mimetype="application/json") // best practice, as then Flask knows it Json

# @app.route('/<genre_name>')
# def by_path(genre_name):
#     # These next two lines are relevant if testing in a reaol browser not in the IDE.
#     # if genre_name.lower() == "favicon.ico":
#     #     return Response("[]", mimetype="application/json")
#     print(request.args.get("genre"))
#     data = movie_filter(genre_name)
#     return json.dumps(data)


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080)

# app.py
from flask import Flask, request, Response, render_template_string
import json
from my_csv_parser import movie_filter

app = Flask(__name__)

# --- JSON endpoints ---
@app.route("/")
def root():
    genre = request.args.get("genre", "").strip()
    data = movie_filter(genre)
    return Response(json.dumps(data), mimetype="application/json")

@app.route("/<genre_name>")
def by_path(genre_name):
    # remove noisy print(None) from favicon requests
    if genre_name.lower() == "favicon.ico":
        return Response("", mimetype="image/x-icon")
    data = movie_filter(genre_name)
    return Response(json.dumps(data), mimetype="application/json")

# --- Simple browser UI (server-side rendered to avoid quoting issues) ---
@app.route("/ui")
def ui():
    html = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>IMDB Browser</title>
  <style>
    body{font-family:system-ui,sans-serif;margin:24px}
    input,button{font-size:16px;padding:6px 8px}
    #results{margin-top:12px}
    .error{color:#b00}
  </style>
</head>
<body>
  <h1>Browse IMDB by Genre</h1>
  <input id="genre" placeholder="e.g. action, romance, western">
  <button id="go">Search</button>
  <button id="quick">Try “romance”</button>
  <p id="status"></p>
  <ul id="results"></ul>
  <script>
    const input = document.getElementById('genre');
    const go = document.getElementById('go');
    const quick = document.getElementById('quick');
    const statusEl = document.getElementById('status');
    const list = document.getElementById('results');

    async function run(g){
      statusEl.textContent = 'Loading…';
      list.innerHTML = '';
      try {
        const res = await fetch('/?genre=' + encodeURIComponent(g));
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const data = await res.json();
        statusEl.textContent = 'Found ' + data.length + ' movies for "' + g + '".';
        for (const row of data) {
          const li = document.createElement('li');
          li.textContent = (row.Title || '(no title)') + ' (' + (row.Year || '?') + ') — ' + (row.Genre || '');
          list.appendChild(li);
        }
      } catch (e) {
        console.error(e);
        statusEl.innerHTML = '<span class="error">Error loading data. See console.</span>';
      }
    }

    go.addEventListener('click', () => {
      const g = (input.value || '').trim();
      if (g) run(g);
    });

    quick.addEventListener('click', () => {
      input.value = 'romance';
      run('romance');
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') go.click();
    });
  </script>
</body>
</html>"""
    return render_template_string(html)  # sends as text/html

# Optional: quiet the favicon noise explicitly
@app.route("/favicon.ico")
def favicon():
    return Response("", mimetype="image/x-icon")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

