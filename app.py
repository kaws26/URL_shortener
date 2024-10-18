from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import random
import string

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# Connect to the SQLite database
def get_db():
    conn = sqlite3.connect('url_shortener.db')
    conn.row_factory = sqlite3.Row
    return conn

# Generate a random short code
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Validate URL
def is_valid_url(url):
    return url.startswith('http://') or url.startswith('https://')

# Main page
@app.route('/')
def index():
    return render_template('index.html')

# URL Shortener route
@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['original_url'].strip()
    
    # Check if URL is valid
    if not is_valid_url(original_url):
        flash("Invalid URL. Please include http:// or https://", 'danger')
        return redirect(url_for('index'))
    
    conn = get_db()
    short_code = generate_short_code()

    try:
        # Insert shortened URL into the database
        conn.execute('INSERT INTO urls (original_url, short_code) VALUES (?, ?)', (original_url, short_code))
        conn.commit()
        short_url = request.url_root + short_code
        flash(f"Shortened URL: {short_url}", 'success')
    except sqlite3.IntegrityError:
        flash("Error shortening the URL. Please try again.", 'danger')
    
    conn.close()
    return render_template('index.html', short_url=short_url)

# Redirection route
@app.route('/<short_code>')
def redirect_to_url(short_code):
    conn = get_db()
    cur = conn.execute('SELECT original_url, clicks FROM urls WHERE short_code = ?', (short_code,))
    row = cur.fetchone()

    if row:
        original_url, clicks = row
        # Increment click count
        conn.execute('UPDATE urls SET clicks = ? WHERE short_code = ?', (clicks + 1, short_code))
        conn.commit()
        conn.close()
        
        # Redirect to the original URL
        return redirect(original_url)
    else:
        flash("Invalid URL", 'danger')
        conn.close()
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
