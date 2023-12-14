import sqlite3
from user import User
from ad import Ad
from datetime import datetime

class AdBoard:
    def __init__(self):
        self.conn = sqlite3.connect("ad.db")  # Connect to the SQLite database (ad.db)
        self.create_tables()
        self.current_user = None

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)

            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS ads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    contact_info TEXT NOT NULL,
                    category TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)

    def register(self, username, password):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            print("Registration successful! You can now log in.")

    def login(self, username, password):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user_data = cursor.fetchone()
            if user_data:
                self.current_user = User(user_data[0], user_data[1], user_data[2])
                print(f"Welcome, {username}!")
            else:
                print("Invalid username or password.")

    def post_ad(self, title, description, contact_info, category):
        if not self.current_user:
            print("Please log in to post an ad.")
            return

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO ads (title, description, contact_info, category, user_id)
                VALUES (?, ?, ?, ?, ?)
            """, (title, description, contact_info, category, self.current_user.id))

            print("Ad posted successfully!")

    def edit_ad(self, ad_id, title, description, contact_info, category):
        if not self.current_user:
            print("Please log in to edit an ad.")
            return

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE ads
                SET title = ?, description = ?, contact_info = ?, category = ?
                WHERE id = ? AND user_id = ?
            """, (title, description, contact_info, category, ad_id, self.current_user.id))

            if cursor.rowcount > 0:
                print("Ad updated successfully.")
            else:
                print("Ad not found or you do not have permission to edit it.")

    def delete_ad(self, ad_id):
        if not self.current_user:
            print("Please log in to delete an ad.")
            return

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM ads WHERE id = ? AND user_id = ?", (ad_id, self.current_user.id))

            if cursor.rowcount > 0:
                print("Ad deleted successfully.")
            else:
                print("Ad not found or you do not have permission to delete it.")

    def view_ads(self, page, sort_by, keyword=""):
        with self.conn:
            cursor = self.conn.cursor()
            if sort_by == "timestamp":
                order_by = "timestamp"
            elif sort_by == "category":
                order_by = "category"
            else:
                order_by = "timestamp"

            query = f"""
                SELECT * FROM ads
                WHERE title LIKE ? OR description LIKE ?
                ORDER BY {order_by}
                LIMIT ? OFFSET ?
            """

            offset = (page - 1) * 10  # Adjust the limit as needed
            cursor.execute(query, (f"%{keyword}%", f"%{keyword}%", 10, offset))
            ads = cursor.fetchall()

            if not ads:
                print("No ads found.")
            else:
                print("Ads:")
                for ad in ads:
                    print(f"Ad #{ad[0]}")
                    print(f"Title: {ad[1]}")
                    print(f"Description: {ad[2]}")
                    print(f"Contact Info: {ad[3]}")
                    print(f"Category: {ad[4]}")
                    print(f"Timestamp: {ad[5]}")
                    print("---------------")

    def view_my_ads(self):
        if not self.current_user:
            print("Please log in to view your ads.")
            return

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM ads WHERE user_id = ?", (self.current_user.id,))
            ads = cursor.fetchall()

            if not ads:
                print("You have no ads posted.")
            else:
                print("Your ads:")
                for ad in ads:
                    print(f"Ad #{ad[0]}")
                    print(f"Title: {ad[1]}")
                    print(f"Description: {ad[2]}")
                    print(f"Contact Info: {ad[3]}")
                    print(f"Category: {ad[4]}")
                    print(f"Timestamp: {ad[5]}")
                    print("---------------")

    def search_ads_by_keyword(self, keyword):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM ads
                WHERE title LIKE ? OR description LIKE ?
            """, (f"%{keyword}%", f"%{keyword}%"))
            ads = cursor.fetchall()

            if not ads:
                print("No ads found.")
            else:
                print("Ads:")
                for ad in ads:
                    print(f"Ad #{ad[0]}")
                    print(f"Title: {ad[1]}")
                    print(f"Description: {ad[2]}")
                    print(f"Contact Info: {ad[3]}")
                    print(f"Category: {ad[4]}")
                    print(f"Timestamp: {ad[5]}")
                    print("---------------")

    def logout(self):
        self.current_user = None
        print("Logout successful.")

    def quit(self):
        print("Thank you for using the Ad Board. Goodbye!")
        self.conn.close()
        exit()

if __name__ == "__main__":
    ad_board = AdBoard()
