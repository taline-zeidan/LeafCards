from flask import Flask, render_template, jsonify, session, request
import sqlite3

app = Flask(__name__)
app.secret_key = '8fc1a05cf18fd2b60d3befb6e475a0008f0e55568bffd4b3d45b6fb699465338'

@app.route('/')
def index():
    return render_template('MyLeafsets.html')

@app.route('/get_user_leafsets/<int:user_id>')
def get_user_leafsets(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        return jsonify({'error': 'Unauthorized or not logged in'}), 401

    try:
        conn = sqlite3.connect('leafcards.db')
        cursor = conn.cursor()
        query = """
        SELECT Leaf_Set_ID, FolderName, Label
        FROM Leaf_Sets
        WHERE UserID = ?
        """
        cursor.execute(query, (user_id,))
        leafsets = cursor.fetchall()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
        return jsonify({'error': 'Database error'}), 500
    finally:
        if conn:
            conn.close()

    return jsonify(leafsets)

@app.route('/get_leafset_cards/<int:folderId>')
def get_leafset_cards(folderId):
    try:
        conn = sqlite3.connect('leafcards.db')
        cursor = conn.cursor()
        query = """
        SELECT Leaf_Card_ID, Leaf_Card_Name, Question, Answer, Knowledge
        FROM Leaf_Cards
        WHERE FolderID = ?
        """
        cursor.execute(query, (folderId,))
        cards = cursor.fetchall()
        return jsonify(cards)
    except sqlite3.Error as error:
        print("Failed to read cards from sqlite table", error)
        return jsonify({'error': 'Database error'}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/update_knowledge', methods=['POST'])
def update_knowledge():
    # Extract card ID and knowledge value from the POST request
    card_id = request.json.get('cardId')
    knowledge = request.json.get('knowledge')

    # Connect to the database and update the knowledge field
    try:
        conn = sqlite3.connect('leafcards.db')
        cursor = conn.cursor()
        query = "UPDATE Leaf_Cards SET Knowledge = ? WHERE Leaf_Card_ID = ?"
        cursor.execute(query, (knowledge, card_id))
        conn.commit()
    except sqlite3.Error as error:
        print("Failed to update knowledge", error)
        return jsonify({'error': 'Database error'}), 500
    finally:
        if conn:
            conn.close()

    # Return a success message
    return jsonify({'success': True})

# Other application code...

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/save_leafset', methods=['POST'])
def save_leafset():
    leafset_name = request.form.get('leafsetName')
    questions = request.form.getlist('questions[]')
    answers = request.form.getlist('answers[]')
    cards = [{'key': q, 'value': a} for q, a in zip(questions, answers)]
    

    if not leafset_name or not cards:
        return jsonify({'error': 'Missing name or cards'}), 400
    
    try:
        with sqlite3.connect('leafcards.db') as conn:
            
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Leaf_Sets (Name) VALUES (?)", (leafset_name,))
            
            leafset_id = cursor.lastrowid
            cursor.executemany("INSERT IN TO Leaf_Cards (Leafset_ID, Question, Answer, Knowledge) VALUES (?,?,?,0)",
                               [(leafset_id, card['key'], card['value']) for card in cards])
            
            conn.commit()
    except sqlite3.Error as e:
        error_info = str(e)
        print(error_info)  
        return jsonify({'error': 'Database error', 'details': error_info}), 500

    return jsonify({'success': True, 'leafset_id': leafset_id}), 200
