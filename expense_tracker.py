import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import csv
from db import add_expense, get_expenses, delete_expense, update_expense
from db import get_budget, set_budget
from PIL import Image, ImageTk  # Import the required library for handling images


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("900x600")
        self.root.configure(bg="#e6f2ff")

        # Call the welcome page first
        self.show_welcome_page()

    def show_welcome_page(self):
        self.welcome_frame = tk.Frame(self.root, bg="#e6f2ff")
        self.welcome_frame.pack(fill="both", expand=True)

        # Add a Canvas for background image
        self.canvas = tk.Canvas(self.welcome_frame, width=900, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Load and set the background image
        self.bg_image = Image.open(r"E:\Python\expensive\expense.jpg")  # Use correct file path
        self.bg_image = self.bg_image.resize((1600, 800), Image.LANCZOS)  # Use Image.LANCZOS for resizing
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Welcome message with larger, bolder font
        self.canvas.create_text(450, 150, text="Welcome to Personal Expense Tracker",
                                                font=("Arial", 30, "bold"), fill="#0000FF")

        # Start button with bigger size and new color
        start_button = tk.Button(self.welcome_frame, text="Start", font=("Arial", 16, "bold"), 
                                 bg="#003366", fg="white", width=12, command=self.show_main_app)
        self.canvas.create_window(450, 350, anchor="center", window=start_button)

    def show_main_app(self):
        self.welcome_frame.destroy()

        style = ttk.Style()
        style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, font=("Arial", 12))
        style.map("Treeview", background=[("selected", "#003366")])

        self.title_label = tk.Label(self.root, text="Personal Expense Tracker", 
                                    font=("Arial", 24, "bold"), bg="#e6f2ff", fg="#003366")
        self.title_label.pack(pady=10)

        # Treeview inside a frame with padding
        self.tree_frame = tk.Frame(self.root, bg="#f0f0f5")
        self.tree_frame.pack(pady=10)

        self.tree = ttk.Treeview(self.tree_frame, columns=("Date", "Category", "Amount", "Description"), show="headings", height=12)
        for col in ("Date", "Category", "Amount", "Description"):
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, anchor="center", width=200)
        self.tree.pack(side="left", fill="both")

        # Scrollbar for the treeview
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Align buttons more attractively in the center
        self.button_frame = tk.Frame(self.root, bg="#e6f2ff")
        self.button_frame.pack(pady=20)

        buttons = [
            ("Add Expense", self.open_add_window),
            ("Edit Selected", self.edit_expense),
            ("Delete Selected", self.delete_expense),
            ("Show Graph", self.show_graph),
            ("Calculate Sum", self.calculate_sum),
            ("Pie Chart", self.show_pie_chart),
            ("Export CSV", self.export_to_csv),
            ("Check Budget", self.check_budget),
            ("Search", self.search_expenses),
            ("Set Budget", self.set_budget_window)
        ]

        for idx, (text, command) in enumerate(buttons):
            tk.Button(self.button_frame, text=text, font=("Arial", 12), bg="#003366", fg="white", 
                      width=12, height=2, command=command).grid(row=0, column=idx, padx=10, pady=10)

        self.load_data()

    def open_add_window(self):
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Add Expense")
        labels = ["Date (YYYY-MM-DD):", "Category:", "Amount:", "Description:"]
        self.entries = []

        for idx, label in enumerate(labels):
            tk.Label(self.add_window, text=label).grid(row=idx, column=0, padx=10, pady=5)
            entry = ttk.Entry(self.add_window)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            self.entries.append(entry)

        tk.Button(self.add_window, text="Add", command=self.add_expense).grid(row=len(labels), column=1, pady=10)

    def add_expense(self):
        data = [entry.get() for entry in self.entries]
        add_expense(*data)
        self.load_data()
        self.add_window.destroy()

    def edit_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Select an item", "Please select an item to edit.")
            return
        item = self.tree.item(selected_item)
        values = item['values']
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Edit Expense")
        self.entries = []

        for idx, value in enumerate(values):
            tk.Label(self.edit_window, text=["Date (YYYY-MM-DD):", "Category:", "Amount:", "Description:"][idx]).grid(row=idx, column=0, padx=10, pady=5)
            entry = ttk.Entry(self.edit_window)
            entry.insert(0, value)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            self.entries.append(entry)

        tk.Button(self.edit_window, text="Save", command=lambda: self.save_changes(selected_item)).grid(row=len(values), column=1, pady=10)

    def save_changes(self, selected_item):
        item = self.tree.item(selected_item)
        old_values = item['values']
        new_values = [entry.get() for entry in self.entries]
        update_expense(*old_values, *new_values)
        self.load_data()
        self.edit_window.destroy()

    def delete_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Select an item", "Please select an item to delete.")
            return
        delete_expense(*self.tree.item(selected_item)['values'])
        self.load_data()

    def calculate_sum(self):
        total_sum = sum(float(self.tree.item(item)['values'][2]) for item in self.tree.selection())
        messagebox.showinfo("Total Sum", f"Total Sum of Selected Expenses: {total_sum}")

    def show_graph(self):
        expenses = get_expenses()
        categories, amounts = zip(*[(expense[1], float(expense[2])) for expense in expenses])
        plt.figure(figsize=(10, 5))
        plt.bar(categories, amounts, color="skyblue")
        plt.xlabel("Category")
        plt.ylabel("Amount")
        plt.title("Expenses by Category")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def show_pie_chart(self):
        expenses = get_expenses()
        categories = {}
        for expense in expenses:
            category, amount = expense[1], float(expense[2])
            categories[category] = categories.get(category, 0) + amount
        
        plt.figure(figsize=(6, 6))
        plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Expense Breakdown by Category')
        plt.show()

    def export_to_csv(self):
        expenses = get_expenses()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Category", "Amount", "Description"])
                writer.writerows(expenses)
            messagebox.showinfo("Export Success", f"Expenses exported to {file_path}.")

    def set_budget_window(self):
        self.budget_window = tk.Toplevel(self.root)
        self.budget_window.title("Set Budget")

        tk.Label(self.budget_window, text="Set Monthly Budget:").grid(row=0, column=0, padx=10, pady=10)
        self.budget_entry = ttk.Entry(self.budget_window)
        self.budget_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.budget_window, text="Set", command=self.set_budget).grid(row=1, column=1, pady=10)

    def set_budget(self):
        try:
            new_budget = float(self.budget_entry.get())
            set_budget(new_budget)  # Call the function to save the budget in the database
            messagebox.showinfo("Success", f"New budget set to {new_budget}.")
            self.budget_window.destroy()
            
            # Automatically check the budget after setting it
            self.check_budget()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the budget.")

    def check_budget(self):
        try:
            expenses = get_expenses()
            total_spent = sum(float(expense[2]) for expense in expenses)  # Sum of expenses
        
            budget = get_budget()  # Fetch the budget from the database

            # Ensure the retrieved budget is a valid number
            if budget is None:
                raise ValueError("Budget not set. Please set a budget first.")

            # Convert budget to float if necessary
            budget = float(budget)

            current_available_balance = budget - total_spent

            if total_spent > budget:
                messagebox.showwarning("Budget Exceeded", f"You have exceeded your monthly budget of {budget}!\nTotal spent: {total_spent}")
            else:
                messagebox.showinfo("Budget Status", f"Total spent: {total_spent}.\nYou are within your budget of {budget}.\nAvailable balance: {current_available_balance}.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while checking the budget: {str(e)}")
            
    def search_expenses(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Expenses")
        labels = ["Category:", "Min Amount:", "Max Amount:"]
        entries = []

        for idx, label in enumerate(labels):
            tk.Label(search_window, text=label).grid(row=idx, column=0, padx=10, pady=5)
            entry = ttk.Entry(search_window)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries.append(entry)

        tk.Button(search_window, text="Search", command=lambda: self.perform_search(*[entry.get() for entry in entries])).grid(row=len(labels), column=1, pady=10)
        
        # Add a "Reset" button to reset the search and show all expenses
        tk.Button(search_window, text="Reset", command=self.reset_expenses).grid(row=len(labels) + 1, column=1, pady=10)

    def perform_search(self, category, min_amount, max_amount):
        expenses = get_expenses()
        filtered_expenses = [
            expense for expense in expenses
            if (not category or category.lower() in expense[1].lower()) and
            (not min_amount or float(expense[2]) >= float(min_amount)) and
            (not max_amount or float(expense[2]) <= float(max_amount))
        ]

        for row in self.tree.get_children():
            self.tree.delete(row)
        for expense in filtered_expenses:
            self.tree.insert("", tk.END, values=expense)

    def reset_expenses(self):
        # Reload all expenses from the database
        self.load_data()
       

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        for expense in get_expenses():
            self.tree.insert("", tk.END, values=expense)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()

