import os

from mistelaflask import create_app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    _app = create_app()
    _app.run(host="0.0.0.0", port=port)
