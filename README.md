# todo-docker-app

Simple Flask TODO app with file-backed storage.

Getting started (local):

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the app locally:

```bash
python3 app.py
```

The app will be available at http://127.0.0.1:5000

Running with Docker:

1. Build the image:

```bash
docker build -t todo-docker-app .
```

2. Run the container:

```bash
docker run --rm -p 5000:5000 -v "$PWD":/app todo-docker-app
```

Using docker-compose:

```bash
docker-compose up --build
```

Notes:
- Tasks are stored in `tasks.txt` in the repository root (bind-mounting the project into the container preserves tasks).
- The app reads `PORT` and `DEBUG` from environment variables when run inside a container.
# todo-docker-app