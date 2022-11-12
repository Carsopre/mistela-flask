import os

from mistelaflask import main

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4242))
    main.run(host="0.0.0.0", port=port)
