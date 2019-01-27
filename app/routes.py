from app import app


@app.route('/')
@app.route('/index')
def index():
    return 'OK'


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    return 'OK'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return 'OK'


@app.route('/signout')
def signout():
    return 'OK'


@app.route('/account', methods=['GET', 'POST'])
def account():
    return 'OK'


@app.route('/dashboard')
def dashboard():
    return 'OK'


@app.route('/notes')
def notes():
    return 'OK'


@app.route('/note/add', methods=['GET', 'POST'])
def add_note():
    return 'OK'


@app.route('/note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    return 'OK'
