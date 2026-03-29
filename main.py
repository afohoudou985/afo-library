import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime
from tkinter import font as tkfont
import hashlib
from tkinter.simpledialog import Dialog
from tkinter.simpledialog import Dialog, askstring  # Add askstring here

# Database Connection
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='library_system'
    )
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET status = LOWER(status)")
    conn.commit()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Failed to connect to database: {err}")
    exit()

# Custom Dialog for Add Book
class AddBookDialog(Dialog):
    def __init__(self, parent, title):
        self.result = None
        super().__init__(parent, title)
    
    def body(self, master):
        self.configure(bg='#f0f8ff')
        
        self.label_font = tkfont.Font(family="Arial", size=10)
        self.entry_font = tkfont.Font(family="Arial", size=10)
        
        Label(master, text="Book ID:", font=self.label_font, bg='#f0f8ff').grid(row=0, sticky=W, pady=5)
        self.book_id = Entry(master, font=self.entry_font)
        self.book_id.grid(row=0, column=1, padx=5, pady=5)
        
        Label(master, text="Title:", font=self.label_font, bg='#f0f8ff').grid(row=1, sticky=W, pady=5)
        self.title = Entry(master, font=self.entry_font)
        self.title.grid(row=1, column=1, padx=5, pady=5)
        
        Label(master, text="Author:", font=self.label_font, bg='#f0f8ff').grid(row=2, sticky=W, pady=5)
        self.author = Entry(master, font=self.entry_font)
        self.author.grid(row=2, column=1, padx=5, pady=5)
        
        Label(master, text="ISBN:", font=self.label_font, bg='#f0f8ff').grid(row=3, sticky=W, pady=5)
        self.isbn = Entry(master, font=self.entry_font)
        self.isbn.grid(row=3, column=1, padx=5, pady=5)
        
        return self.book_id
    
    def validate(self):
        if not self.book_id.get() or not self.title.get() or not self.author.get() or not self.isbn.get():
            messagebox.showwarning("Validation", "All fields are required!")
            return False
        
        try:
            int(self.book_id.get())
        except ValueError:
            messagebox.showwarning("Validation", "Book ID must be a number!")
            return False
            
        return True
    
    def apply(self):
        self.result = (
            int(self.book_id.get()),
            self.title.get(),
            self.author.get(),
            self.isbn.get()
        )

# Custom Dialog for Issue Book
class IssueBookDialog(Dialog):
    def __init__(self, parent, title, book_title):
        self.book_title = book_title
        self.result = None
        super().__init__(parent, title)
    
    def body(self, master):
        self.configure(bg='#f0f8ff')
        
        self.label_font = tkfont.Font(family="Arial", size=10)
        self.entry_font = tkfont.Font(family="Arial", size=10)
        
        Label(master, text=f"Issuing: {self.book_title}", font=self.label_font, 
              bg='#f0f8ff', fg='#2c3e50').grid(row=0, columnspan=2, pady=10)
        
        Label(master, text="Borrower Name:", font=self.label_font, bg='#f0f8ff').grid(row=1, sticky=W, pady=5)
        self.borrower = Entry(master, font=self.entry_font)
        self.borrower.grid(row=1, column=1, padx=5, pady=5)
        
        return self.borrower
    
    def validate(self):
        if not self.borrower.get():
            messagebox.showwarning("Validation", "Borrower name is required!")
            return False
        return True
    
    def apply(self):
        self.result = self.borrower.get()

# Main Application Class
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f8ff')
        self.current_user = None
        
        self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        self.button_font = tkfont.Font(family="Arial", size=10, weight="bold")
        self.label_font = tkfont.Font(family="Arial", size=10)
        
        self.create_login_frame()
    
    def create_login_frame(self):
        self.clear_window()
        
        bg_frame = Frame(self.root, bg='#3498db')
        bg_frame.pack(fill=BOTH, expand=True)
        
        self.login_frame = Frame(bg_frame, bg='white', bd=2, relief=RAISED)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=500)
        
        logo_frame = Frame(self.login_frame, bg='white', height=100)
        logo_frame.pack(fill=X, pady=(30, 10))
        
        Label(logo_frame, text="📚", font=("Arial", 50), bg='white').pack()
        Label(logo_frame, text="LIBRARY SYSTEM", font=self.title_font, bg='white', fg='#2c3e50').pack(pady=10)
        
        self.notebook = ttk.Notebook(self.login_frame)
        self.notebook.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        self.login_tab = Frame(self.notebook, bg='white')
        self.notebook.add(self.login_tab, text='Login')
        self.create_login_form(self.login_tab)
        
        self.signup_tab = Frame(self.notebook, bg='white')
        self.notebook.add(self.signup_tab, text='Sign Up')
        self.create_signup_form(self.signup_tab)
    
    def create_login_form(self, parent):
        form_frame = Frame(parent, bg='white')
        form_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)
        
        Label(form_frame, text="Username:", font=self.label_font, bg='white').grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.login_username = Entry(form_frame, font=self.label_font, width=25, bd=1, relief=SOLID)
        self.login_username.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        
        Label(form_frame, text="Password:", font=self.label_font, bg='white').grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.login_password = Entry(form_frame, font=self.label_font, width=25, show='*', bd=1, relief=SOLID)
        self.login_password.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        
        login_btn = Button(form_frame, text="Login", font=self.button_font, 
                          command=self.handle_login, bg='#3498db', fg='white',
                          activebackground='#2980b9', activeforeground='white',
                          padx=20, pady=8, borderwidth=0, bd=0, highlightthickness=0)
        login_btn.grid(row=2, columnspan=2, pady=20, sticky='ew')
        
        self.login_password.bind('<Return>', lambda event: self.handle_login())
    
    def create_signup_form(self, parent):
        form_frame = Frame(parent, bg='white')
        form_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)
        
        Label(form_frame, text="Username:", font=self.label_font, bg='white').grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.signup_username = Entry(form_frame, font=self.label_font, width=25, bd=1, relief=SOLID)
        self.signup_username.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        
        Label(form_frame, text="Password:", font=self.label_font, bg='white').grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.signup_password = Entry(form_frame, font=self.label_font, width=25, show='*', bd=1, relief=SOLID)
        self.signup_password.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        
        Label(form_frame, text="Confirm Password:", font=self.label_font, bg='white').grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.signup_confirm = Entry(form_frame, font=self.label_font, width=25, show='*', bd=1, relief=SOLID)
        self.signup_confirm.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
        
        signup_btn = Button(form_frame, text="Sign Up", font=self.button_font, 
                           command=self.handle_signup, bg='#2ecc71', fg='white',
                           activebackground='#27ae60', activeforeground='white',
                           padx=20, pady=8, borderwidth=0)
        signup_btn.grid(row=3, columnspan=2, pady=20, sticky='ew')
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def handle_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        hashed_password = self.hash_password(password)
        
        try:
            cursor.execute("SELECT user_id FROM users WHERE username = %s AND password = %s", 
                         (username, hashed_password))
            user = cursor.fetchone()
            
            if user:
                self.current_user = {'id': user[0], 'username': username}
                self.create_main_interface()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to login: {e}")
    
    def handle_signup(self):
        username = self.signup_username.get().strip()
        password = self.signup_password.get().strip()
        confirm = self.signup_confirm.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
            
        hashed_password = self.hash_password(password)
        
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                         (username, hashed_password))
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully! Please login.")
            self.notebook.select(self.login_tab)
            self.login_username.delete(0, END)
            self.login_password.delete(0, END)
            self.signup_username.delete(0, END)
            self.signup_password.delete(0, END)
            self.signup_confirm.delete(0, END)
            self.login_username.insert(0, username)
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to create account: {e}")
    
    def create_main_interface(self):
        self.clear_window()
        
        header_frame = Frame(self.root, bg='#2c3e50', padx=20, pady=15)
        header_frame.pack(fill=X)
        
        Label(header_frame, 
              text=f"Welcome, {self.current_user['username']}!", 
              font=self.title_font, 
              bg='#2c3e50', 
              fg='white').pack(side=LEFT)
        
        logout_btn = Button(header_frame, text="Logout", font=self.button_font,
                           command=self.logout, bg='#e74c3c', fg='white',
                           activebackground='#c0392b', activeforeground='white',
                           padx=15, pady=3, borderwidth=0)
        logout_btn.pack(side=RIGHT)
        
        main_frame = Frame(self.root, bg='#f0f8ff')
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        search_frame = Frame(main_frame, bg='#f0f8ff', bd=1, relief=SOLID, padx=10, pady=10)
        search_frame.pack(fill=X, pady=10)
        
        Label(search_frame, text="Search Book:", 
              font=self.label_font, bg='#f0f8ff').pack(side=LEFT)
        
        self.search_var = StringVar()
        self.entry_search = Entry(search_frame, font=self.label_font, width=40,
                                textvariable=self.search_var, bd=1, relief=SOLID)
        self.entry_search.pack(side=LEFT, padx=10, fill=X, expand=True)
        
        search_btn = Button(search_frame, text="Search", font=self.button_font,
                          command=self.search_books, bg='#3498db', fg='white',
                          activebackground='#2980b9', activeforeground='white',
                          padx=15, pady=3, borderwidth=0)
        search_btn.pack(side=LEFT, padx=5)
        
        reset_btn = Button(search_frame, text="Reset", font=self.button_font,
                         command=self.refresh_book_list, bg='#95a5a6', fg='white',
                         activebackground='#7f8c8d', activeforeground='white',
                         padx=15, pady=3, borderwidth=0)
        reset_btn.pack(side=LEFT)
        
        tree_frame = Frame(main_frame, bg='#f0f8ff', bd=1, relief=SOLID)
        tree_frame.pack(fill=BOTH, expand=True, pady=10)
        
        columns = ('Book ID', 'Title', 'Author', 'ISBN', 'Status')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                       background="#ffffff", 
                       foreground="#2c3e50",
                       rowheight=30,
                       fieldbackground="#ffffff",
                       font=self.label_font)
        style.configure("Treeview.Heading", 
                       background="#3498db", 
                       foreground="white",
                       font=self.button_font)
        style.map('Treeview', background=[('selected', '#2980b9')])
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=40, width=150, anchor='center')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        button_frame = Frame(main_frame, bg='#f0f8ff')
        button_frame.pack(fill=X, pady=10)
        
        self.btn_add = Button(button_frame, text="Add Book", font=self.button_font,
                            command=self.add_book, bg='#2ecc71', fg='white',
                            activebackground='#27ae60', activeforeground='white',
                            padx=15, pady=8, borderwidth=0)
        self.btn_add.pack(side=LEFT, padx=5)
        
        self.btn_delete = Button(button_frame, text="Delete Book", font=self.button_font,
                               command=self.delete_book, bg='#e74c3c', fg='white',
                               activebackground='#c0392b', activeforeground='white',
                               padx=15, pady=8, borderwidth=0)
        self.btn_delete.pack(side=LEFT, padx=5)
        
        self.btn_issue = Button(button_frame, text="Issue Book", font=self.button_font,
                              command=self.issue_book, bg='#3498db', fg='white',
                              activebackground='#2980b9', activeforeground='white',
                              padx=15, pady=8, borderwidth=0)
        self.btn_issue.pack(side=LEFT, padx=5)
        
        self.btn_return = Button(button_frame, text="Return Book", font=self.button_font,
                               command=self.return_book, bg='#9b59b6', fg='white',
                               activebackground='#8e44ad', activeforeground='white',
                               padx=15, pady=8, borderwidth=0)
        self.btn_return.pack(side=LEFT, padx=5)
        
        Label(main_frame, text="Issued Books:", font=self.label_font, 
             bg='#f0f8ff', fg='#2c3e50').pack(anchor='w', pady=(20, 5))
        
        issued_frame = Frame(main_frame, bg='#f0f8ff', bd=1, relief=SOLID)
        issued_frame.pack(fill=BOTH, expand=True)
        
        columns_issued = ('Issue ID', 'Book ID', 'Title', 'Borrower Name', 'Issue Date')
        self.tree_issued = ttk.Treeview(issued_frame, columns=columns_issued, show='headings', height=7)
        
        for col in columns_issued:
            self.tree_issued.heading(col, text=col)
            self.tree_issued.column(col, minwidth=40, width=120, anchor='center')
        
        scrollbar_issued = ttk.Scrollbar(issued_frame, orient="vertical", command=self.tree_issued.yview)
        self.tree_issued.configure(yscrollcommand=scrollbar_issued.set)
        self.tree_issued.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar_issued.pack(side=RIGHT, fill=Y)
        
        self.status_var = StringVar()
        self.status_var.set("Ready")
        status_bar = Label(self.root, textvariable=self.status_var, bd=1, relief=SUNKEN, 
                          anchor=W, bg='#2c3e50', fg='white', font=self.label_font)
        status_bar.pack(side=BOTTOM, fill=X)
        
        self.refresh_book_list()
        self.refresh_issued_list()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def logout(self):
        self.current_user = None
        self.create_login_frame()
    
    def refresh_book_list(self):
        self.status_var.set("Refreshing book list...")
        self.root.update()
        
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        try:
            cursor.execute("SELECT book_id, title, author, isbn, status FROM books ORDER BY book_id")
            books = cursor.fetchall()
            
            if not books:
                self.status_var.set("No books found in database")
                return
                
            for book in books:
                self.tree.insert('', END, values=book)
                
            self.status_var.set(f"Loaded {len(books)} books")
        except mysql.connector.Error as e:
            self.status_var.set("Error loading books")
            messagebox.showerror("Database Error", f"Failed to load books: {e}")
    
    def add_book(self):
        dialog = AddBookDialog(self.root, "Add New Book")
        
        if dialog.result:
            book_id, title, author, isbn = dialog.result
            
            cursor.execute("SELECT book_id FROM books WHERE book_id = %s", (book_id,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Book ID already exists.")
                return
                
            cursor.execute("SELECT isbn FROM books WHERE isbn = %s", (isbn,))
            if cursor.fetchone():
                messagebox.showerror("Error", "ISBN already exists.")
                return

            try:
                cursor.execute("""
                    INSERT INTO books (book_id, title, author, isbn, status) 
                    VALUES (%s, %s, %s, %s, 'available')
                """, (book_id, title, author, isbn))
                conn.commit()
                messagebox.showinfo("Success", "Book added successfully.")
                self.refresh_book_list()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to add book: {e}")
    
    def delete_book(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to delete.")
            return
            
        book = self.tree.item(selected)['values']
        book_id = book[0]
        status = book[4]
        
        if status == 'issued':
            messagebox.showwarning("Warning", "Cannot delete a book that is currently issued.")
            return

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete book ID {book_id}?"):
            try:
                cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
                conn.commit()
                messagebox.showinfo("Success", "Book deleted successfully.")
                self.refresh_book_list()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to delete book: {e}")
    
    def issue_book(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to issue.")
            return
            
        book = self.tree.item(selected)['values']
        book_id, title, author, isbn, status = book

        if status == 'issued':
            messagebox.showinfo("Info", "This book is already issued.")
            return
            
        dialog = IssueBookDialog(self.root, "Issue Book", title)
        
        if dialog.result:
            borrower_name = dialog.result
            
            try:
                cursor.execute("SELECT status FROM books WHERE book_id = %s", (book_id,))
                current_status = cursor.fetchone()[0]
                
                if current_status != 'available':
                    messagebox.showwarning("Warning", "This book is no longer available for issue.")
                    return
                    
                issue_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                cursor.callproc('issue_book', (book_id, borrower_name))
                conn.commit()
                
                messagebox.showinfo("Success", f"Book '{title}' issued to {borrower_name}")
                    
                self.refresh_book_list()
                self.refresh_issued_list()
            except mysql.connector.Error as e:
                conn.rollback()
                messagebox.showerror("Error", f"Failed to issue book: {e}")
    
    def return_book(self):

        """Return an issued book with proper error handling"""
        try:
            # Ask for ISBN
            isbn = askstring("Return Book", "Enter ISBN of the book to return:", parent=self.root)  # Use askstring directly
            if not isbn or isbn.strip() == "":
                messagebox.showwarning("Input Error", "ISBN cannot be empty!")
                return
            
            # Ask for Borrower Name
            borrower_name = askstring("Return Book", "Enter Borrower's Name:", parent=self.root)  # Use askstring directly
            if not borrower_name or borrower_name.strip() == "":
                messagebox.showwarning("Input Error", "Borrower name cannot be empty!")
                return
        

            # Verify book exists
            cursor.execute("SELECT book_id, title, status FROM books WHERE isbn = %s", (isbn,))
            book_data = cursor.fetchone()
            
            if not book_data:
                messagebox.showerror("Not Found", "No book found with this ISBN!")
                return
                
            book_id, title, status = book_data
            
            # Check if book is actually issued
            if status != 'issued':
                messagebox.showwarning("Status Error", "This book is not currently issued!")
                return

            # Verify this borrower has this book issued
            cursor.execute("""
                SELECT issue_id FROM issued_books 
                WHERE book_id = %s AND borrower_name = %s
            """, (book_id, borrower_name))
            
            issue_record = cursor.fetchone()
            
            if not issue_record:
                messagebox.showerror("Not Found", 
                    f"No issued record found for borrower '{borrower_name}' with this book!")
                return
                
            issue_id = issue_record[0]

            # Perform the return
            try:
                cursor.execute("DELETE FROM issued_books WHERE issue_id = %s", (issue_id,))
                cursor.execute("UPDATE books SET status = 'available' WHERE book_id = %s", (book_id,))
                conn.commit()
                
                messagebox.showinfo("Success", 
                    f"Book '{title}' (ID: {book_id}) successfully returned by {borrower_name}.")
                    
                # Refresh displays
                self.refresh_book_list()
                self.refresh_issued_list()
                
            except mysql.connector.Error as e:
                conn.rollback()
                messagebox.showerror("Database Error", f"Failed to complete return: {e}")
                
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
    
    def search_books(self):
        keyword = self.search_var.get().strip()
        
        if not keyword:
            self.refresh_book_list()
            return
            
        self.status_var.set(f"Searching for: {keyword}")
        self.root.update()
        
        keyword = f"%{keyword}%"
        
        try:
            cursor.execute("""
                SELECT book_id, title, author, isbn, status 
                FROM books 
                WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s
                ORDER BY title
            """, (keyword, keyword, keyword))
            
            results = cursor.fetchall()
            
            for row in self.tree.get_children():
                self.tree.delete(row)
                
            if results:
                for book in results:
                    self.tree.insert('', END, values=book)
                self.status_var.set(f"Found {len(results)} matching books")
            else:
                self.status_var.set("No books found matching search criteria")
                messagebox.showinfo("No Results", "No books found matching your search.")
        except mysql.connector.Error as e:
            self.status_var.set("Search error")
            messagebox.showerror("Database Error", f"Failed to search books: {e}")
    
    def refresh_issued_list(self):
        self.status_var.set("Refreshing issued books list...")
        self.root.update()
        
        for row in self.tree_issued.get_children():
            self.tree_issued.delete(row)
            
        try:
            cursor.execute("""
                SELECT ib.issue_id, b.book_id, b.title, ib.borrower_name, ib.issue_date
                FROM issued_books ib 
                JOIN books b ON ib.book_id = b.book_id 
                ORDER BY ib.issue_date DESC
            """)
            
            issued_books = cursor.fetchall()
            
            if not issued_books:
                self.status_var.set("No books currently issued")
                return
                
            for issued in issued_books:
                issue_date = issued[4].strftime("%Y-%m-%d %H:%M:%S") if issued[4] else "N/A"
                
                self.tree_issued.insert('', END, values=(
                    issued[0], issued[1], issued[2], issued[3], issue_date
                ))
                
            self.status_var.set(f"Loaded {len(issued_books)} issued books")
        except mysql.connector.Error as e:
            self.status_var.set("Error loading issued books")
            messagebox.showerror("Database Error", f"Failed to load issued books: {e}")

# Run the application
if __name__ == "__main__":
    root = Tk()
    app = LibraryApp(root)
    
    # Center the window
    window_width = 1200
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    root.mainloop()