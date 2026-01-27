from apps import app
import os

### Run Main ======================================== 
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('PORT'))