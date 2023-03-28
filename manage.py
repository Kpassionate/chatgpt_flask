from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
