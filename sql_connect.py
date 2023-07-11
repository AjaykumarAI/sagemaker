import mysql.connector
import datetime

def store_conversation(cnx, user_id, session_id, user_message, chatbot_message):
    # Prepare SQL statement
    sql = "INSERT INTO conversations (date_time, user_id, session_id, user_message, chatbot_message) VALUES (%s, %s, %s, %s, %s)"
    values = (datetime.datetime.now(), user_id, session_id, user_message, chatbot_message)

    # Create cursor and execute SQL statement
    cursor = cnx.cursor()
    cursor.execute(sql, values)

    # Commit changes
    cnx.commit()
    cursor.close()

# Establish database connection
cnx = mysql.connector.connect(
    host='localhost',
    user='rasa',
    password='rasa123',
    database='rasa'
)

# Example usage
user_id = "john.doe@example.com"
session_id = "12345"
user_message = "Hello!"

msg = Message(message=user_message, session_id=session_id)
response = # call webservice which you integrated previously     you have to pass session id, and user id and user message and bot response to store values to db
store_conversation(cnx, user_id=user_id, session_id=session_id, user_message=user_message, chatbot_message=response)
cnx.close()


