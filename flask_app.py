from flask import url_for
from app import app


if __name__ == '__main__':
    with app.test_request_context():
        print(url_for('login'))
        print(url_for('login', next='/'))
        print(url_for('profile', user_id='John Doe'))   
    # app.run(debug=True)
    # Alt. runner properly for Code, where there is no need to use the in-browser debugger or the reloader
    app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)