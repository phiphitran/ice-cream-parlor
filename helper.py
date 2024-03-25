import json
import sqlite3
from transformers import pipeline

def connect_db():
    """
    Connects to database and returns the connection object
    and cursor for data traversal.
    """
    conn = sqlite3.connect('data/flavors_small.db')
    cursor = conn.cursor()
    return conn, cursor

def check_menu():
    """
    Retrieves the menu of ice creams.
    """
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM ICECREAM;")
    ans = cursor.fetchall()
    cursor.close()
    conn.close()

    menu = [a[1] for a in ans]
    return json.dumps({'menu': menu})

def check_inventory():
    """
    Retrieves the inventory of ice creams.
    """
    conn, cursor = connect_db()
    cursor.execute("SELECT FLAVOR, QUANTITY FROM ICECREAM;")
    inventory = cursor.fetchall()
    cursor.close()
    conn.close()
    return json.dumps({'inventory': inventory})

def purchase_ice_cream(input_flavor, input_quantity):
    """
    Updates changes in database if the flavor and its quantity 
    that customer want to purchase exists. 
    """
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM ICECREAM;")
    data = cursor.fetchall()

    customer_flavor = input_flavor
    customer_quantity = input_quantity
    menu = [flavor[1] for flavor in data]
    for id_, flavor, price, quantity in data:
        if customer_flavor == flavor and customer_quantity > quantity:
            error_msgs = f"Sorry, we are out of stock of your flavor. The number of scoops we currently have is {flavor}:{quantity}"
            return json.dumps({'error': error_msgs})
    if customer_flavor not in menu:
        error_msgs = f"Sorry, we don't seem to have the {flavor} flavor right now"
        return json.dumps({'error': error_msgs})
    else:
        cursor.execute(f"UPDATE ICECREAM SET QUANTITY = QUANTITY - {customer_quantity} WHERE FLAVOR = ?", (customer_flavor,))

    conn.commit()
    cursor.close()
    conn.close()
    success_message = f"Order placed successfully."
    return json.dumps({'message': success_message})

def restock_ice_cream(restock_flavor, restock_quantity):
    """
    Updates changes in database if the quantity of the new restocked flavor is less than 20.
    """
    conn, cursor = connect_db()
    cursor.execute("SELECT FLAVOR, QUANTITY FROM ICECREAM;")
    data = cursor.fetchall()
    new_id = len(data) + 1

    if not any(restock_flavor in f[0] for f in data):
        if restock_quantity > 20:
            error_msgs = f"Sorry, this is too much ice cream. We can only have 20 of one flavor at a time."
            return json.dumps({'error': error_msgs})
        else:
            cursor.execute("INSERT INTO ICECREAM VALUES (?,?, 10, ?)", (new_id, restock_flavor, restock_quantity))
    else:
        for current_flavor, current_quantity in data:
            if (restock_flavor == current_flavor):
                if (current_quantity + restock_quantity) <= 20:
                    cursor.execute("UPDATE ICECREAM SET QUANTITY = QUANTITY + ? WHERE FLAVOR = ?", (restock_quantity, restock_flavor))
                else:
                    error_msgs = f"Sorry, we already have {current_quantity} scoops of this flavor and can only have 20 in total."
                    return json.dumps({'error': error_msgs})

    conn.commit()
    cursor.close()
    conn.close()
    return json.dumps({'message': 'Ice cream restocked successfully.'})

def give_user_feedback(user_feedback, user_rating):
    """
    Adds user feedback and rating to the feedback table in database.
    """
    conn, cursor = connect_db()

    cursor.execute("SELECT COUNT(*) FROM feedback_table;")
    count = cursor.fetchall()
    cursor.execute("INSERT INTO feedback_table VALUES (?,?,?)", (count[0][0]+1, user_feedback, user_rating))

    conn.commit()
    cursor.close()
    conn.close()
    return json.dumps({'message': 'Feedback has been received, thank you for sharing!'})

def get_all_feedback():
    """
    Retrieves all customer feedback.
    """
    conn, cursor = connect_db()

    cursor.execute("SELECT feedback, rating FROM feedback_table;")
    all_feedback = cursor.fetchall()

    cursor.close()
    conn.close()
    return json.dumps({'feedback': all_feedback})

def feedback_report():
    """
    Extracts feedback data and retrieves a summary report.
    """
    conn, cursor = connect_db()

    cursor.execute("SELECT ROUND(AVG(rating)) AS average_rating, COUNT(*) AS num_respondents FROM feedback_table;")
    result = cursor.fetchall()

    avg_rating = result[0][0]
    num_respondents = result[0][1]

    positive_count, negative_count = get_sentiment_counts(cursor)

    cursor.close()
    conn.close()
    return json.dumps({'feedback_summary': 'An overview of the reviews from our ice cream',
                'number_respondents': num_respondents,
                'average_rating': avg_rating,
                'positive sentiments': positive_count,
                'negative sentiments': negative_count})

def get_sentiment_counts(cursor):
    """
    Performs sentiment analysis of the customer feedback.
    """
    # Retrieve customer feedback data
    cursor.execute("SELECT feedback FROM feedback_table")
    feedback_data = cursor.fetchall()

    feedback_texts = [feedback[0].lower() for feedback in feedback_data]

    sentiment_analysis = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

    # Perform sentiment analysis on each feedback
    feedback_sentiments = []
    for text in feedback_texts:
        sentiment = sentiment_analysis(text)[0]
        feedback_sentiments.append(sentiment)

    positive_count = 0
    negative_count = 0

    # Count positive and negative sentiments
    for sentiment in feedback_sentiments:
        if sentiment['label'] == 'POSITIVE':
            positive_count += 1
        elif sentiment['label'] == 'NEGATIVE':
            negative_count += 1
    
    return positive_count, negative_count