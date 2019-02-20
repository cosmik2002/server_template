from srv import create_app, db
from srv.models import User

app = create_app()

@app.shell_context_processor
def make_shell_context():
    print("123")
    return {'db': db, 'User': User}