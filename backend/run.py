from app import create_app
from app.config.database import setup_indexes

app = create_app()

if __name__ == '__main__':
    setup_indexes()  # Setup MongoDB indexes
    app.run(debug=True, host='0.0.0.0', port=5000) 

