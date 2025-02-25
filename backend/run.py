import os
from flask import Flask, send_from_directory
from app import create_app

app = create_app()

# Ensure Flask serves from `/app/static`
BASE_DIR = os.path.dirname(os.path.abspath(__name__))  # Get `/app`
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')  # `/app/static`
app.static_folder = STATIC_FOLDER  # Force Flask to use `/app/static`

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    print(f" Flask Requested: {path}")
    print(f" Serving from: {os.path.join(STATIC_FOLDER, path)}")

    if path and os.path.exists(os.path.join(STATIC_FOLDER, path)):
        return send_from_directory(STATIC_FOLDER, path)

    return send_from_directory(STATIC_FOLDER, 'index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
