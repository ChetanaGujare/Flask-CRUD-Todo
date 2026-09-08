from flask import request, jsonify
from db import get_db_connection, close_connection

def register_routes(app):

    @app.route('/api/todos', methods=['GET'])
    def get_todos():
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM todos ORDER BY id DESC")
            todos = cursor.fetchall()
            return jsonify({'success': True, 'data': todos}), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            close_connection(conn, cursor)

    @app.route('/api/todos/<int:todo_id>', methods=['GET'])
    def get_todo(todo_id):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
            todo = cursor.fetchone()
            if not todo:
                return jsonify({'success': False, 'error': 'Todo not found'}), 404
            return jsonify({'success': True, 'data': todo}), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            close_connection(conn, cursor)

    @app.route('/api/todos', methods=['POST'])
    def create_todo():
        data = request.get_json()
        if not data or 'title' not in data or not data['title'].strip():
            return jsonify({'success': False, 'error': 'Title is required'}), 400
        title = data['title'].strip()
        description = data.get('description', '').strip()
        completed = data.get('completed', False)
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO todos (title, description, completed) VALUES (%s, %s, %s)",
                (title, description, completed)
            )
            conn.commit()
            new_id = cursor.lastrowid
            return jsonify({'success': True, 'id': new_id}), 201
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            close_connection(conn, cursor)

    @app.route('/api/todos/<int:todo_id>', methods=['PUT'])
    def update_todo(todo_id):
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        allowed_fields = {'title', 'description', 'completed'}
        updates = {}
        for field in allowed_fields:
            if field in data:
                updates[field] = data[field]
        if not updates:
            return jsonify({'success': False, 'error': 'No valid fields'}), 400
        set_clause = ', '.join([f"{key} = %s" for key in updates.keys()])
        values = list(updates.values())
        values.append(todo_id)
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f"UPDATE todos SET {set_clause} WHERE id = %s", values)
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({'success': False, 'error': 'Todo not found'}), 404
            return jsonify({'success': True}), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            close_connection(conn, cursor)

    @app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
    def delete_todo(todo_id):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({'success': False, 'error': 'Todo not found'}), 404
            return jsonify({'success': True}), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            close_connection(conn, cursor)