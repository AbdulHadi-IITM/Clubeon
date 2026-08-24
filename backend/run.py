import os

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Debug must never be on in production: the Werkzeug debugger allows
    # arbitrary code execution. Opt in locally with FLASK_DEBUG=1.
    debug = os.environ.get('FLASK_DEBUG', '').lower() in ('1', 'true', 'yes')
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5001))
    app.run(host=host, debug=debug, port=port)