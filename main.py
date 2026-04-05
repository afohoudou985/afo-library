import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime
from tkinter import font as tkfont
import hashlib
from tkinter.simpledialog import Dialog
from tkinter.simpledialog import Dialog, askstring  # Add askstring here

# Connexion à la base de données
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
    messagebox.showerror("Erreur de base de données", f"Échec de la connexion à la base de données : {err}")
    exit()

# Boîte de dialogue personnalisée pour ajouter un livre
class AddBookDialog(Dialog):
    def __init__(self, parent, title):
        self.result = None
        super().__init__(parent, title)
    
    def body(self, master):
        self.configure(bg='#f0f8ff')
        
        self.label_font = tkfont.Font(family="Arial", size=10)
        self.entry_font = tkfont.Font(family="Arial", size=10)
        
        Label(master, text="ID du livre :", font=self.label_font, bg='#f0f8ff').grid(row=0, sticky=W, pady=5)
        self.book_id = Entry(master, font=self.entry_font)
        self.book_id.grid(row=0, column=1, padx=5, pady=5)
        
        Label(master, text="Titre :", font=self.label_font, bg='#f0f8ff').grid(row=1, sticky=W, pady=5)
        self.title = Entry(master, font=self.entry_font)
        self.title.grid(row=1, column=1, padx=5, pady=5)
        
        Label(master, text="Auteur :", font=self.label_font, bg='#f0f8ff').grid(row=2, sticky=W, pady=5)
        self.author = Entry(master, font=self.entry_font)
        self.author.grid(row=2, column=1, padx=5, pady=5)
        
        Label(master, text="ISBN :", font=self.label_font, bg='#f0f8ff').grid(row=3, sticky=W, pady=5)
        self.isbn = Entry(master, font=self.entry_font)
        self.isbn.grid(row=3, column=1, padx=5, pady=5)
        
        return self.book_id
    
    def validate(self):
        if not self.book_id.get() or not self.title.get() or not self.author.get() or not self.isbn.get():
            messagebox.showwarning("Validation", "Tous les champs sont obligatoires !")
            return False
        
        try:
            int(self.book_id.get())
        except ValueError:
            messagebox.showwarning("Validation", "L’ID du livre doit être un nombre !")
            return False
            
        return True
    
    def apply(self):
        self.result = (
            int(self.book_id.get()),
            self.title.get(),
            self.author.get(),
            self.isbn.get()
        )

# Boîte de dialogue personnalisée pour l’emprunt d’un livre
class IssueBookDialog(Dialog):
    def __init__(self, parent, title, book_title):
        self.book_title = book_title
        self.result = None
        super().__init__(parent, title)
    
    def body(self, master):
        self.configure(bg='#f0f8ff')
        
        self.label_font = tkfont.Font(family="Arial", size=10)
        self.entry_font = tkfont.Font(family="Arial", size=10)
        
        Label(master, text=f"Emprunt : {self.book_title}", font=self.label_font, 
              bg='#f0f8ff', fg='#2c3e50').grid(row=0, columnspan=2, pady=10)
        
        Label(master, text="Nom de l’emprunteur :", font=self.label_font, bg='#f0f8ff').grid(row=1, sticky=W, pady=5)
        self.borrower = Entry(master, font=self.entry_font)
        self.borrower.grid(row=1, column=1, padx=5, pady=5)
        
        return self.borrower
    
    def validate(self):
        if not self.borrower.get():
            messagebox.showwarning("Validation", "Le nom de l’emprunteur est obligatoire !")
            return False
        return True
    
    def apply(self):
        self.result = self.borrower.get()

# Main Application Class
class LibraryApp:
  def __init__(self, root):
    self.root = root
    self.root.title("Système de Gestion de Bibliothèque")
    self.root.geometry("1200x800")
    self.root.configure(bg='#f0f8ff')
    self.current_user = None

    # Définition des polices
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

    # Section logo
    logo_frame = Frame(self.login_frame, bg='white', height=100)
    logo_frame.pack(fill=X, pady=(30, 10))

    Label(logo_frame, text="📚", font=("Arial", 50), bg='white').pack()
    Label(logo_frame, text="SYSTÈME DE BIBLIOTHÈQUE",
    font=self.title_font, bg='white', fg='#2c3e50').pack(pady=10)

    # Notebook (onglets)
    self.notebook = ttk.Notebook(self.login_frame)
    self.notebook.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # Onglet Connexion
    self.login_tab = Frame(self.notebook, bg='white')
    self.notebook.add(self.login_tab, text='Connexion')
    self.create_login_form(self.login_tab)

    # Onglet Inscription
    self.signup_tab = Frame(self.notebook, bg='white')
    self.notebook.add(self.signup_tab, text='Inscription')
    self.create_signup_form(self.signup_tab)


  def create_login_form(self, parent):
    form_frame = Frame(parent, bg='white')
    form_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

    Label(form_frame, text="Nom d'utilisateur :",
    font=self.label_font, bg='white').grid(row=0, column=0, padx=10, pady=10, sticky='w')

    self.login_username = Entry(form_frame, font=self.label_font, width=25, bd=1, relief=SOLID)
    self.login_username.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

    Label(form_frame, text="Mot de passe :",
    font=self.label_font, bg='white').grid(row=1, column=0, padx=10, pady=10, sticky='w')

    self.login_password = Entry(form_frame, font=self.label_font, width=25, show='*', bd=1, relief=SOLID)
    self.login_password.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

    login_btn = Button(form_frame, text="Se connecter", font=self.button_font,
    command=self.handle_login, bg='#3498db', fg='white',
    activebackground='#2980b9', activeforeground='white',
    padx=20, pady=8, borderwidth=0, bd=0, highlightthickness=0)
    login_btn.grid(row=2, columnspan=2, pady=20, sticky='ew')

    # Permet de valider avec la touche Entrée
    self.login_password.bind('<Return>', lambda event: self.handle_login())


  def create_signup_form(self, parent):
    form_frame = Frame(parent, bg='white')
    form_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

    Label(form_frame, text="Nom d'utilisateur :",
    font=self.label_font, bg='white').grid(row=0, column=0, padx=10, pady=10, sticky='w')

    self.signup_username = Entry(form_frame, font=self.label_font, width=25, bd=1, relief=SOLID)
    self.signup_username.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

    Label(form_frame, text="Mot de passe :",
    font=self.label_font, bg='white').grid(row=1, column=0, padx=10, pady=10, sticky='w')

    self.signup_password = Entry(form_frame, font=self.label_font, width=25, show='*', bd=1, relief=SOLID)
    self.signup_password.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

    Label(form_frame, text="Confirmer le mot de passe :",
    font=self.label_font, bg='white').grid(row=2, column=0, padx=10, pady=10, sticky='w')

    self.signup_confirm = Entry(form_frame, font=self.label_font, width=25, show='*', bd=1, relief=SOLID)
    self.signup_confirm.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

    signup_btn = Button(form_frame, text="S'inscrire", font=self.button_font,
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
        messagebox.showerror("Erreur", "Veuillez saisir le nom d'utilisateur et le mot de passe")
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
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe invalide")

    except mysql.connector.Error as e:
        messagebox.showerror("Erreur Base de données", f"Échec de la connexion : {e}")


  def handle_signup(self):
    username = self.signup_username.get().strip()
    password = self.signup_password.get().strip()
    confirm = self.signup_confirm.get().strip()

    if not username or not password:
        messagebox.showerror("Erreur", "Veuillez saisir le nom d'utilisateur et le mot de passe")
        return

    if password != confirm:
        messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas")
        return

    if len(password) < 6:
        messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 6 caractères")
        return

    hashed_password = self.hash_password(password)

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, hashed_password))
        conn.commit()

        messagebox.showinfo("Succès", "Compte créé avec succès ! Veuillez vous connecter.")

        # Retour à l'onglet Connexion et pré-remplissage du nom d'utilisateur
        self.notebook.select(self.login_tab)
        self.login_username.delete(0, END)
        self.login_password.delete(0, END)
        self.signup_username.delete(0, END)
        self.signup_password.delete(0, END)
        self.signup_confirm.delete(0, END)
        self.login_username.insert(0, username)

    except mysql.connector.IntegrityError:
        messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà")
    except mysql.connector.Error as e:
        messagebox.showerror("Erreur Base de données", f"Échec de la création du compte : {e}")


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
      self.status_var.set("Actualisation de la liste des livres...")
      self.root.update()

      # Supprimer toutes les lignes existantes
      for row in self.tree.get_children():
          self.tree.delete(row)

          try:
              cursor.execute("SELECT book_id, title, author, isbn, status FROM books ORDER BY book_id")
              books = cursor.fetchall()

              if not books:
                  self.status_var.set("Aucun livre trouvé dans la base de données")
                  return

              for book in books:
                  self.tree.insert('', END, values=book)

                  self.status_var.set(f"{len(books)} livres chargés")

          except mysql.connector.Error as e:
              self.status_var.set("Erreur lors du chargement des livres")
              messagebox.showerror("Erreur Base de données", f"Impossible de charger les livres : {e}")


  def add_book(self):
      dialog = AddBookDialog(self.root, "Ajouter un nouveau livre")
      if dialog.result:
          book_id, title, author, isbn = dialog.result

          # Vérification si le Book ID existe déjà
          cursor.execute("SELECT book_id FROM books WHERE book_id = %s", (book_id,))
          if cursor.fetchone():
              messagebox.showerror("Erreur", "Cet ID de livre existe déjà.")
              return

          # Vérification si l'ISBN existe déjà
          cursor.execute("SELECT isbn FROM books WHERE isbn = %s", (isbn,))
          if cursor.fetchone():
              messagebox.showerror("Erreur", "Cet ISBN existe déjà.")
              return

          try:
              cursor.execute("""
              INSERT INTO books (book_id, title, author, isbn, status)
              VALUES (%s, %s, %s, %s, 'available')
              """, (book_id, title, author, isbn))
              conn.commit()
              messagebox.showinfo("Succès", "Livre ajouté avec succès.")
              self.refresh_book_list()
          except mysql.connector.Error as e:
              messagebox.showerror("Erreur", f"Impossible d'ajouter le livre : {e}")


  def delete_book(self):
      selected = self.tree.focus()
      if not selected:
          messagebox.showwarning("Attention", "Veuillez sélectionner un livre à supprimer.")
          return

      book = self.tree.item(selected)['values']
      book_id = book[0]
      status = book[4]

      if status == 'issued':
          messagebox.showwarning("Attention", "Impossible de supprimer un livre actuellement emprunté.")
          return

      if messagebox.askyesno("Confirmation de suppression",
      f"Êtes-vous sûr de vouloir supprimer le livre ID {book_id} ?"):
          try:
              cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
              conn.commit()
              messagebox.showinfo("Succès", "Livre supprimé avec succès.")
              self.refresh_book_list()
          except mysql.connector.Error as e:
              messagebox.showerror("Erreur", f"Impossible de supprimer le livre : {e}")


  def issue_book(self):
      selected = self.tree.focus()
      if not selected:
          messagebox.showwarning("Attention", "Veuillez sélectionner un livre à emprunter.")
          return

      book = self.tree.item(selected)['values']
      book_id, title, author, isbn, status = book

      if status == 'issued':
          messagebox.showinfo("Information", "Ce livre est déjà emprunté.")
          return

      dialog = IssueBookDialog(self.root, "Emprunter un livre", title)
      if dialog.result:
          borrower_name = dialog.result

          try:
              # Vérification du statut actuel
              cursor.execute("SELECT status FROM books WHERE book_id = %s", (book_id,))
              current_status = cursor.fetchone()[0]

              if current_status != 'available':
                  messagebox.showwarning("Attention", "Ce livre n'est plus disponible à l'emprunt.")
                  return

              # Appel de la procédure stockée pour l'emprunt
              issue_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
              cursor.callproc('issue_book', (book_id, borrower_name))
              conn.commit()

              messagebox.showinfo("Succès", f"Le livre '{title}' a été emprunté par {borrower_name}")

              self.refresh_book_list()
              self.refresh_issued_list()

          except mysql.connector.Error as e:
              conn.rollback()
              messagebox.showerror("Erreur", f"Impossible d'emprunter le livre : {e}")


  def return_book(self):
      """Retourner un livre emprunté avec gestion des erreurs"""
      try:
          # Demander l'ISBN
          isbn = askstring("Retourner un livre", "Entrez l'ISBN du livre à retourner :", parent=self.root)
          if not isbn or isbn.strip() == "":
              messagebox.showwarning("Erreur de saisie", "L'ISBN ne peut pas être vide !")
              return

          # Demander le nom de l'emprunteur
          borrower_name = askstring("Retourner un livre", "Entrez le nom de l'emprunteur :", parent=self.root)
          if not borrower_name or borrower_name.strip() == "":
              messagebox.showwarning("Erreur de saisie", "Le nom de l'emprunteur ne peut pas être vide !")
              return

          # Vérifier si le livre existe
          cursor.execute("SELECT book_id, title, status FROM books WHERE isbn = %s", (isbn,))
          book_data = cursor.fetchone()
          if not book_data:
              messagebox.showerror("Non trouvé", "Aucun livre trouvé avec cet ISBN !")
              return

          book_id, title, status = book_data

          # Vérifier que le livre est bien emprunté
          if status != 'issued':
              messagebox.showwarning("Erreur de statut", "Ce livre n'est pas actuellement emprunté !")
              return

          # Vérifier que cet emprunteur a bien ce livre
          cursor.execute("""
          SELECT issue_id FROM issued_books
          WHERE book_id = %s AND borrower_name = %s
          """, (book_id, borrower_name))
          issue_record = cursor.fetchone()

          if not issue_record:
              messagebox.showerror("Non trouvé",
              f"Aucun enregistrement d'emprunt trouvé pour {borrower_name} avec ce livre !")
              return

          issue_id = issue_record[0]

          # Effectuer le retour
          try:
              cursor.execute("DELETE FROM issued_books WHERE issue_id = %s", (issue_id,))
              cursor.execute("UPDATE books SET status = 'available' WHERE book_id = %s", (book_id,))
              conn.commit()

              messagebox.showinfo("Succès",
              f"Le livre '{title}' (ID: {book_id}) a été retourné par {borrower_name} avec succès.")

              # Rafraîchir les affichages
              self.refresh_book_list()
              self.refresh_issued_list()

          except mysql.connector.Error as e:
              conn.rollback()
              messagebox.showerror("Erreur Base de données", f"Impossible d'effectuer le retour : {e}")

      except Exception as e:
          messagebox.showerror("Erreur", f"Une erreur inattendue s'est produite : {str(e)}")
          
  def search_books(self):
      keyword = self.search_var.get().strip()

      if not keyword:
          self.refresh_book_list()
          return

      self.status_var.set(f"Recherche en cours pour : {keyword}")
      self.root.update()

      # Préparation du motif de recherche (LIKE)
      keyword = f"%{keyword}%"

      try:
          cursor.execute("""
          SELECT book_id, title, author, isbn, status
          FROM books
          WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s
          ORDER BY title
          """, (keyword, keyword, keyword))

          results = cursor.fetchall()

          # Supprimer les anciennes lignes du tableau
          for row in self.tree.get_children():
              self.tree.delete(row)

              if results:
                  for book in results:
                      self.tree.insert('', END, values=book)
                      self.status_var.set(f"{len(results)} livre(s) trouvé(s)")
              else:
                  self.status_var.set("Aucun livre ne correspond à votre recherche")
                  messagebox.showinfo("Aucun résultat", "Aucun livre ne correspond à vos critères de recherche.")

      except mysql.connector.Error as e:
          self.status_var.set("Erreur lors de la recherche")
          messagebox.showerror("Erreur Base de données", f"Impossible d'effectuer la recherche : {e}")


  def refresh_issued_list(self):
      self.status_var.set("Actualisation de la liste des livres empruntés...")
      self.root.update()

      # Supprimer toutes les lignes existantes
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
                  self.status_var.set("Aucun livre n'est actuellement emprunté")
                  return

              for issued in issued_books:
                  # Formatage de la date si elle existe
                  issue_date = issued[4].strftime("%Y-%m-%d %H:%M:%S") if issued[4] else "N/A"
                  self.tree_issued.insert('', END, values=(
                      issued[0], issued[1], issued[2], issued[3], issue_date
                  ))

                  self.status_var.set(f"{len(issued_books)} livre(s) emprunté(s) chargé(s)")

          except mysql.connector.Error as e:
              self.status_var.set("Erreur lors du chargement des livres empruntés")
              messagebox.showerror("Erreur Base de données", f"Impossible de charger les livres empruntés : {e}")
            
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