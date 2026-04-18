from app.db.database import get_connection


def create_appeal(user_id, full_name, username, category, message, is_anonymous):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO appeals (user_id, full_name, username, category, message, is_anonymous)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, full_name, username, category, message, int(is_anonymous)))

    appeal_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return appeal_id


def create_question(user_id, full_name, username, question):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO questions (user_id, full_name, username, question)
        VALUES (?, ?, ?, ?)
    """, (user_id, full_name, username, question))

    question_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return question_id


def get_appeal_by_id(appeal_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appeals WHERE id = ?", (appeal_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_question_by_id(question_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def reply_to_appeal(appeal_id: int, reply_text: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE appeals
        SET admin_reply = ?, status = 'answered', replied_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (reply_text, appeal_id))
    conn.commit()
    conn.close()


def reply_to_question(question_id: int, reply_text: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE questions
        SET admin_reply = ?, status = 'answered', replied_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (reply_text, question_id))
    conn.commit()
    conn.close()