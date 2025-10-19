import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")  


BG_COLOR = "#F5F5F5"
SIDEBAR_COLOR = "#E0F7FA"
BUTTON_COLOR = "#00796B"
TEXT_COLOR = "#212121"
ENTRY_COLOR = "#FFFFFF"

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Finance Tracker")
        self.geometry("1000x600")
        self.configure(fg_color=BG_COLOR)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.income = 0
        self.expense = 0
        self.income_transactions = [] 
        self.expense_transactions = []

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=SIDEBAR_COLOR)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Finance Tracker", 
                                       font=ctk.CTkFont(size=28, weight="bold"), text_color=TEXT_COLOR)
        self.logo_label.pack(pady=(30, 20))

        self.income_button = ctk.CTkButton(self.sidebar_frame, text="Income", command=self.income_button_event,
                                           fg_color=BUTTON_COLOR, text_color="white", hover_color="#004D40")
        self.income_button.pack(pady=10)

        self.expenses_button = ctk.CTkButton(self.sidebar_frame, text="Expenses", command=self.expenses_button_event,
                                             fg_color=BUTTON_COLOR, text_color="white", hover_color="#004D40")
        self.expenses_button.pack(pady=10)

        self.balance_button = ctk.CTkButton(self.sidebar_frame, text="Balance", command=self.balance_button_event,
                                            fg_color=BUTTON_COLOR, text_color="white", hover_color="#004D40")
        self.balance_button.pack(pady=10)

        # Main content
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=BG_COLOR)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.income_frame, self.income_tree = self.create_transaction_frame("Income", self.add_income, self.income_transactions)
        self.expense_frame, self.expense_tree = self.create_transaction_frame("Expense", self.add_expense, self.expense_transactions)
        self.balance_frame = self.create_balance_frame()

        self.hide_frames()
        self.income_frame.pack(fill="both", expand=True)

        # Area
        self.fig = Figure(figsize=(4, 4), dpi=100) 
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.balance_frame)
        self.canvas.get_tk_widget().pack(pady=20)

    def create_transaction_frame(self, title, button_command, transactions):
        frame = ctk.CTkFrame(self.main_frame, fg_color=BG_COLOR)
        ctk.CTkLabel(frame, text=f"Add {title}", font=ctk.CTkFont(size=22, weight="bold"), text_color=TEXT_COLOR).pack(pady=10)

        form_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        form_frame.pack(pady=10)

        ctk.CTkLabel(form_frame, text="Category", text_color=TEXT_COLOR).grid(row=0, column=0, padx=10, pady=5)
        category_entry = ctk.CTkEntry(form_frame, fg_color=ENTRY_COLOR, text_color=TEXT_COLOR, width=200)
        category_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(form_frame, text="Amount", text_color=TEXT_COLOR).grid(row=1, column=0, padx=10, pady=5)
        amount_entry = ctk.CTkEntry(form_frame, fg_color=ENTRY_COLOR, text_color=TEXT_COLOR, width=200)
        amount_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkButton(frame, text=f"Add {title}", command=lambda: button_command(category_entry, amount_entry),
                      fg_color=BUTTON_COLOR, text_color="white", hover_color="#004D40").pack(pady=10)

        tree = ttk.Treeview(frame)
        tree["columns"] = ("Category", "Amount")
        tree.column("#0", width=0, stretch="NO")
        tree.column("Category", anchor="w", width=150)
        tree.column("Amount", anchor="w", width=100)
        tree.heading("Category", text="Category", anchor='w')
        tree.heading("Amount", text="Amount", anchor='w')
        tree.pack(pady=20, fill="x", padx=20)

        return frame, tree

    def create_balance_frame(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color=BG_COLOR)
        ctk.CTkLabel(frame, text="Balance Overview", font=ctk.CTkFont(size=22, weight="bold"), text_color=TEXT_COLOR).pack(pady=10)
        return frame

    def hide_frames(self):
        for frame in [self.income_frame, self.expense_frame, self.balance_frame]:
            frame.pack_forget()

    def income_button_event(self):
        self.hide_frames()
        self.income_frame.pack(fill="both", expand=True)

    def expenses_button_event(self):
        self.hide_frames()
        self.expense_frame.pack(fill="both", expand=True)

    def balance_button_event(self):
        self.hide_frames()
        self.balance_frame.pack(fill="both", expand=True)
        self.update_plot()

    def add_income(self, category_entry, amount_entry):
        amount = self.get_amount_from_entry(amount_entry)
        category = category_entry.get()
        if amount is not None:
            self.income += amount
            self.income_transactions.append((category, amount))
            self.update_table(self.income_tree, self.income_transactions)
            category_entry.delete(0, 'end')
            amount_entry.delete(0, 'end')

    def add_expense(self, category_entry, amount_entry):
        amount = self.get_amount_from_entry(amount_entry)
        category = category_entry.get()
        if amount is not None:
            self.expense += amount
            self.expense_transactions.append((category, amount))
            self.update_table(self.expense_tree, self.expense_transactions)
            category_entry.delete(0, 'end')
            amount_entry.delete(0, 'end')

    def get_amount_from_entry(self, entry):
        try:
            amount = float(entry.get())
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a positive number")
            return None

    def update_plot(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.pie([self.income, self.expense], labels=['Income', 'Expense'], autopct='%1.1f%%')
        self.canvas.draw()

    def update_table(self, tree, transactions):
        for i in tree.get_children():
            tree.delete(i)
        for transaction in transactions:
            tree.insert('', 'end', values=transaction)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
