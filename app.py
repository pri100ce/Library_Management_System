from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
#from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super_secret_library_key"


# ------------------------------
# DATABASE CONNECTION
# ------------------------------
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="prince21",
            database="library_db"
        )
        return conn
    except Error as e:
        print("Database Connection Error:", e)
        return None

def log_activity(message):

    conn = get_db_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute(

        "INSERT INTO activity_logs(activity) VALUES(%s)",

        (message,)

    )

    conn.commit()

    cursor.close()

    conn.close()    


# ------------------------------
# HOME PAGE
# ------------------------------
@app.route('/')
def login_page():
    return render_template("login.html")


# ------------------------------
# LOGIN
# ------------------------------
@app.route('/login', methods=['POST'])
def login():

    role = request.form.get("role")
    username = request.form.get("username")
    password = request.form.get("password")

    conn = get_db_connection()

    if conn is None:
        flash("Database connection failed.")
        return redirect(url_for("login_page"))

    cursor = conn.cursor(dictionary=True)

    try:

        if role == "admin":

            cursor.execute(
                "SELECT * FROM admins WHERE username=%s",
                (username,)
            )

            admin = cursor.fetchone()
            #print("Admin:", admin)

            if admin and admin["password"] == password:

                session["user_id"] = admin["id"]
                session["role"] = "admin"
                session["name"] = admin["username"]

                return redirect(url_for("admin_dashboard"))

        elif role == "student":

            cursor.execute(
                "SELECT * FROM students WHERE id=%s",
                (username,)
            )

            student = cursor.fetchone()
            #print("Student:", student)

            if student and student["password"] == password:

                session["user_id"] = student["id"]
                session["role"] = "student"
                session["name"] = student["name"]

                return redirect(url_for("student_dashboard"))

        flash("Invalid username or password.")
        return redirect(url_for("login_page"))

    finally:
        cursor.close()
        conn.close()


# ------------------------------
# LOGOUT
# ------------------------------
@app.route("/logout")
def logout():

    session.clear()
    #flash("Logged out successfully.")
    return redirect(url_for("login_page"))


# ------------------------------
# ADMIN DASHBOARD
# ------------------------------
@app.route("/admin/dashboard")
def admin_dashboard():

    if session.get("role") != "admin":
        return redirect(url_for("login_page"))

    conn = get_db_connection()

    if conn is None:
        flash("Database connection failed.")
        return redirect(url_for("login_page"))

    cursor = conn.cursor(dictionary=True)

    try:

        # Total Books
        cursor.execute("SELECT COUNT(*) AS total FROM books")
        total_books = cursor.fetchone()["total"]

        # Total Students
        cursor.execute("SELECT COUNT(*) AS total FROM students")
        total_students = cursor.fetchone()["total"]

        # Issued Books
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM issued_books
            WHERE status='Issued'
        """)
        issued_books = cursor.fetchone()["total"]

        # Overdue Books
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM issued_books
            WHERE status='Issued'
            AND return_date < CURDATE()
        """)
        overdue_books = cursor.fetchone()["total"]
        
        cursor.execute("""
        
        SELECT *
        
        FROM activity_logs
        
        ORDER BY id DESC
        
        LIMIT 5
        
        """)
        
        activities = cursor.fetchall()

        return render_template(
            "admin_dashboard.html",
            name=session["name"],
            total_books=total_books,
            total_students=total_students,
            issued_books=issued_books,
            overdue_books=overdue_books,
            activities=activities
        )

    finally:

        cursor.close()
        conn.close()

# ------------------------------
# ADD BOOK
# ------------------------------
@app.route("/admin/add-book", methods=["GET", "POST"])
def add_book():

    if session.get("role") != "admin":
        return redirect(url_for("login_page"))

    if request.method == "POST":

        name = request.form.get("name").strip()
        author = request.form.get("author").strip()
        category = request.form.get("category").strip()

        try:
            quantity = int(request.form.get("qty"))
        except:
            flash("Quantity must be a number.")
            return redirect(url_for("add_book"))

        if quantity < 0:
            flash("Quantity cannot be negative.")
            return redirect(url_for("add_book"))

        conn = get_db_connection()

        if conn is None:
            flash("Database connection failed.")
            return redirect(url_for("add_book"))

        cursor = conn.cursor()

        try:

            cursor.execute("""
                INSERT INTO books
                (book_name, author, category, quantity)
                VALUES(%s,%s,%s,%s)
            """, (name, author, category, quantity))

            conn.commit()
            
            log_activity(f"📚 New book added : {name}")

            flash("Book added successfully.")

            return redirect(url_for("view_books"))

        except Error as e:

            flash(f"Error : {e}")

        finally:

            cursor.close()
            conn.close()

    return render_template("add_book.html")


# ------------------------------
# VIEW / UPDATE / DELETE BOOKS
# ------------------------------
@app.route("/admin/view-books", methods=["GET", "POST"])
def view_books():

    if session.get("role") != "admin":
        return redirect(url_for("login_page"))

    conn = get_db_connection()

    if conn is None:
        flash("Database connection failed.")
        return redirect(url_for("admin_dashboard"))

    cursor = conn.cursor(dictionary=True)

    try:

        if request.method == "POST":

            action = request.form.get("action")
            book_id = request.form.get("id")

            # ---------------- UPDATE ----------------

            if action == "update":

                name = request.form.get("name").strip()
                author = request.form.get("author").strip()
                category = request.form.get("category").strip()

                try:
                    quantity = int(request.form.get("qty"))
                except:
                    flash("Invalid quantity.")
                    return redirect(url_for("view_books"))

                if quantity < 0:
                    flash("Quantity cannot be negative.")
                    return redirect(url_for("view_books"))

                cursor.execute("""
                    UPDATE books
                    SET
                        book_name=%s,
                        author=%s,
                        category=%s,
                        quantity=%s
                    WHERE id=%s
                """,
                (
                    name,
                    author,
                    category,
                    quantity,
                    book_id
                ))

                conn.commit()

                flash("Book updated successfully.")

            # ---------------- DELETE ----------------

            elif action == "delete":

                cursor.execute("""
                    SELECT COUNT(*) AS total
                    FROM issued_books
                    WHERE
                        book_id=%s
                        AND status='Issued'
                """, (book_id,))

                active = cursor.fetchone()

                if active["total"] > 0:

                    flash("Book cannot be deleted because it is currently issued.")

                else:

                    cursor.execute("""
                        DELETE FROM books
                        WHERE id=%s
                    """, (book_id,))

                    conn.commit()
                    
                    log_activity("🗑️ Book deleted.")

                    flash("Book deleted successfully.")

            return redirect(url_for("view_books"))

        # ---------------- SHOW ALL BOOKS ----------------

        cursor.execute("""
            SELECT *
            FROM books
            ORDER BY id DESC
        """)

        books = cursor.fetchall()

        return render_template(
            "view_books.html",
            books=books
        )

    except Error as e:

        flash(f"Error : {e}")

        return redirect(url_for("admin_dashboard"))

    finally:

        cursor.close()
        conn.close()
        
# ------------------------------
# ADD STUDENT
# ------------------------------
@app.route("/admin/add-student", methods=["GET", "POST"])
def add_student():

    if session.get("role") != "admin":
        return redirect(url_for("login_page"))

    if request.method == "POST":

        name = request.form.get("name").strip()
        student_class = request.form.get("class").strip()
        phone = request.form.get("phone").strip()
        password = request.form.get("password")

        # ---------- Validation ----------

        if len(name) < 2:
            flash("Student name is too short.")
            return redirect(url_for("add_student"))

        if not phone.isdigit() or len(phone) != 10:
            flash("Enter a valid 10-digit phone number.")
            return redirect(url_for("add_student"))

        if len(password) < 4:
            flash("Password must contain at least 4 characters.")
            return redirect(url_for("add_student"))

        hashed_password = password

        conn = get_db_connection()

        if conn is None:
            flash("Database connection failed.")
            return redirect(url_for("add_student"))

        cursor = conn.cursor()

        try:

            cursor.execute("""
                INSERT INTO students
                (name, class, phone, password)
                VALUES(%s,%s,%s,%s)
            """,
            (
                name,
                student_class,
                phone,
                hashed_password
            ))

            conn.commit()
            
            log_activity(f"👨 Student registered : {name}")

            flash("Student added successfully.")

            return redirect(url_for("view_students"))

        except Error as e:

            flash(f"Error : {e}")

        finally:

            cursor.close()
            conn.close()

    return render_template("add_student.html")


# ------------------------------
# VIEW / UPDATE / DELETE STUDENTS
# ------------------------------
@app.route("/admin/view-students", methods=["GET", "POST"])
def view_students():

    if session.get("role") != "admin":
        return redirect(url_for("login_page"))

    conn = get_db_connection()

    if conn is None:
        flash("Database connection failed.")
        return redirect(url_for("admin_dashboard"))

    cursor = conn.cursor(dictionary=True)

    try:

        if request.method == "POST":

            action = request.form.get("action")
            student_id = request.form.get("id")

            # ---------------- UPDATE ----------------

            if action == "update":

                name = request.form.get("name").strip()
                student_class = request.form.get("class").strip()
                phone = request.form.get("phone").strip()

                if not phone.isdigit() or len(phone) != 10:
                    flash("Invalid phone number.")
                    return redirect(url_for("view_students"))

                cursor.execute("""
                    UPDATE students
                    SET
                        name=%s,
                        class=%s,
                        phone=%s
                    WHERE id=%s
                """,
                (
                    name,
                    student_class,
                    phone,
                    student_id
                ))

                conn.commit()

                flash("Student updated successfully.")

            # ---------------- DELETE ----------------

            elif action == "delete":

                cursor.execute("""
                    SELECT COUNT(*) AS total
                    FROM issued_books
                    WHERE
                        student_id=%s
                        AND status='Issued'
                """, (student_id,))

                active = cursor.fetchone()

                if active["total"] > 0:

                    flash("Student has issued books. Return them first.")

                else:

                    cursor.execute("""
                        DELETE FROM students
                        WHERE id=%s
                    """, (student_id,))

                    conn.commit()
                    
                    log_activity("🗑️ Student deleted.")
                    

                    flash("Student deleted successfully.")

            return redirect(url_for("view_students"))

        cursor.execute("""
            SELECT *
            FROM students
            ORDER BY id DESC
        """)

        students = cursor.fetchall()

        return render_template(
            "view_students.html",
            students=students
        )

    except Error as e:

        flash(f"Error : {e}")

        return redirect(url_for("admin_dashboard"))

    finally:

        cursor.close()
        conn.close()



# ------------------------------
# ISSUE BOOK
# ------------------------------
@app.route("/admin/issue-book", methods=["GET", "POST"])
def issue_book():

    if session.get("role") != "admin":
        return redirect(url_for("login_page"))

    conn = get_db_connection()

    if conn is None:
        flash("Database connection failed.")
        return redirect(url_for("admin_dashboard"))

    cursor = conn.cursor(dictionary=True)

    try:

        if request.method == "POST":

            student_id = request.form.get("student_id")
            book_id = request.form.get("book_id")
            issue_date = request.form.get("issue_date")
            return_date = request.form.get("return_date")

            cursor.execute(
                "SELECT quantity FROM books WHERE id=%s",
                (book_id,)
            )

            book = cursor.fetchone()

            if not book:
                flash("Book not found.")
                return redirect(url_for("issue_book"))

            if book["quantity"] <= 0:
                flash("Book is out of stock.")
                return redirect(url_for("issue_book"))

            cursor.execute("""
                INSERT INTO issued_books
                (student_id, book_id, issue_date, return_date)
                VALUES(%s,%s,%s,%s)
            """,
            (
                student_id,
                book_id,
                issue_date,
                return_date
            ))

            cursor.execute("""
                UPDATE books
                SET quantity = quantity - 1
                WHERE id=%s
            """, (book_id,))

            conn.commit()
            
            log_activity("📤 A book was issued.")

            flash("Book issued successfully.")

            return redirect(url_for("view_issued_books"))

        cursor.execute("SELECT id, name FROM students")
        students = cursor.fetchall()

        cursor.execute("""
            SELECT id, book_name
            FROM books
            WHERE quantity > 0
        """)

        books = cursor.fetchall()

        return render_template(
            "issue_book.html",
            students=students,
            books=books
        )

    except Error as e:

        flash(str(e))

        return redirect(url_for("admin_dashboard"))

    finally:

        cursor.close()
        conn.close()


# ------------------------------
# VIEW ISSUED BOOKS
# ------------------------------
@app.route("/admin/view-issued")
def view_issued_books():

    if session.get("role") != "admin":
        return redirect(url_for("login_page"))

    conn = get_db_connection()

    if conn is None:
        flash("Database connection failed.")
        return redirect(url_for("admin_dashboard"))

    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute("""
        SELECT
            i.id,
            s.name AS student_name,
            b.book_name,
            i.issue_date,
            i.return_date,
            i.status,
            i.fine_amount
        FROM issued_books i
        JOIN students s ON i.student_id=s.id
        JOIN books b ON i.book_id=b.id
        ORDER BY i.id DESC
        """)

        issued = cursor.fetchall()

        today = datetime.now().date()

        for record in issued:

            if record["status"] == "Issued":

                due = record["return_date"]

                if today > due:

                    fine = (today - due).days * 5

                    cursor.execute("""
                        UPDATE issued_books
                        SET fine_amount=%s
                        WHERE id=%s
                    """,
                    (
                        fine,
                        record["id"]
                    ))

                    record["fine_amount"] = fine

        conn.commit()

        return render_template(
            "view_issued.html",
            issued=issued
        )

    finally:

        cursor.close()
        conn.close()


# ------------------------------
# RETURN BOOK
# ------------------------------
@app.route("/admin/return-book", methods=["GET", "POST"])
def return_book():

    if session.get("role") != "admin":
        return redirect(url_for("login_page"))

    conn = get_db_connection()

    if conn is None:
        flash("Database connection failed.")
        return redirect(url_for("admin_dashboard"))

    cursor = conn.cursor(dictionary=True)

    try:

        if request.method == "POST":

            issued_id = request.form.get("issued_id")

            cursor.execute("""
                SELECT *
                FROM issued_books
                WHERE id=%s
            """,
            (issued_id,)
            )

            issue = cursor.fetchone()

            if not issue:

                flash("Record not found.")
                return redirect(url_for("return_book"))

            today = datetime.now().date()

            fine = 0

            if today > issue["return_date"]:
                fine = (today - issue["return_date"]).days * 5

            cursor.execute("""
                UPDATE issued_books
                SET
                    status='Returned',
                    fine_amount=%s
                WHERE id=%s
            """,
            (
                fine,
                issued_id
            ))

            cursor.execute("""
                UPDATE books
                SET quantity=quantity+1
                WHERE id=%s
            """,
            (
                issue["book_id"],
            ))

            conn.commit()
            
            log_activity("📥 A book was returned.")

            flash("Book returned successfully.")

            return redirect(url_for("view_issued_books"))

        cursor.execute("""
        SELECT
            i.id,
            s.name,
            b.book_name
        FROM issued_books i
        JOIN students s ON i.student_id=s.id
        JOIN books b ON i.book_id=b.id
        WHERE i.status='Issued'
        """)

        active_issues = cursor.fetchall()

        return render_template(
            "return_book.html",
            active_issues=active_issues
        )

    finally:

        cursor.close()
        conn.close()


# ------------------------------
# STUDENT DASHBOARD
# ------------------------------
@app.route("/student/dashboard")
def student_dashboard():

    if session.get("role") != "student":
        return redirect(url_for("login_page"))

    conn = get_db_connection()

    if conn is None:
        flash("Database connection failed.")
        return redirect(url_for("login_page"))

    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute("""
        SELECT
            i.id,
            b.book_name,
            b.author,
            i.issue_date,
            i.return_date,
            i.status,
            i.fine_amount
        FROM issued_books i
        JOIN books b
        ON i.book_id=b.id
        WHERE i.student_id=%s
        ORDER BY i.id DESC
        """,
        (
            session["user_id"],
        ))

        books = cursor.fetchall()

        today = datetime.now().date()

        for book in books:

            if book["status"] == "Issued":

                if today > book["return_date"]:

                    fine = (today-book["return_date"]).days * 5

                    cursor.execute("""
                        UPDATE issued_books
                        SET fine_amount=%s
                        WHERE id=%s
                    """,
                    (
                        fine,
                        book["id"]
                    ))

                    book["fine_amount"] = fine

        conn.commit()

        return render_template(
            "student_dashboard.html",
            name=session["name"],
            books=books
        )

    finally:

        cursor.close()
        conn.close()


# ------------------------------
# MAIN
# ------------------------------
if __name__ == "__main__":
    app.run(debug=False)        