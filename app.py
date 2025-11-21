from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

@app.route('/api/videos')
def get_videos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM videos ORDER BY created_at DESC')
    videos = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify([{
        'id': row[0],
        'url': f"https://api.telegram.org/file/bot{os.getenv('BOT_TOKEN')}/{row[1]}",
        'username': row[2],
        'description': row[3],
        'likes': row[4]
    } for row in videos])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)