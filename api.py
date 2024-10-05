from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)
# Database connection function using PyMySQL
def get_db_connection():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="flask_crud",
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Database connection established successfully")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Route to get all posts
@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM posts')
        posts = cursor.fetchall()
    conn.close()
    return jsonify(posts)

# Route to create a new post
@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    title = data['title']
    content = data['content']

    if not title or not content:
        return jsonify({'error': 'Title and content are required!'}), 400

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO posts (title, content) VALUES (%s, %s)', (title, content))
        conn.commit()
    conn.close()

    return jsonify({'success': 'Post created successfully!'})

# Route to edit a post
@app.route('/<int:id>/edit', methods=['PUT'])
def edit(id):
    data = request.get_json()
    title = data['title']
    content = data['content']

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('UPDATE posts SET title = %s, content = %s WHERE id = %s', (title, content, id))
        conn.commit()
    conn.close()

    return jsonify({'success': 'Post updated successfully!'})

# Route to delete a post
@app.route('/<int:id>/delete', methods=['DELETE'])
def delete(id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM posts WHERE id = %s', (id,))
        conn.commit()
    conn.close()

    return jsonify({'failure': 'Post deleted successfully!'})

if __name__ == "__main__":
    app.run(debug=True)
