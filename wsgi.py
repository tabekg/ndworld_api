from main import app
from utils.config import IS_DEBUG_MODE, PORT

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=IS_DEBUG_MODE, port=PORT)
