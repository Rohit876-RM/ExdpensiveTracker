import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry, Calendar
import pandas as pd
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os
import random

class ModernExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("💸 Extreme Expense & Income Tracker")
        self.root.geometry("1200x800")
        self.root.config(bg="#F2F6FC")

        self.data = []
        self.budget = 5000
        self.dark_mode = False
        self.categories = ["Food", "Transport", "Salary", "Shopping", "Utilities", "Others"]

        self.setup_ui()
        self.load_data()
        self.animate_background()

    def animate_background(self):
        colors = ["#F2F6FC", "#E6F0FF", "#D9ECFF", "#CCE5FF"]
        self.current_color = 0

        def change_color():
            self.root.config(bg=colors[self.current_color])
            self.current_color = (self.current_color + 1) % len(colors)
            self.root.after(4000, change_color)

        change_color()

    def setup_ui(self):
        header = tk.Label(self.root, text="💰 Extreme Expense & Income Tracker", font=("Segoe UI", 24, "bold"), bg="#F2F6FC", fg="#4A6FA5")
        header.pack(pady=20)

        form = tk.Frame(self.root, bg="#F2F6FC")
        form.pack(pady=10)

        tk.Label(form, text="Date:", font=("Segoe UI", 12), bg="#F2F6FC").grid(row=0, column=0, padx=10)
        self.date_entry = DateEntry(form, width=12)
        self.date_entry.grid(row=0, column=1, padx=5)

        tk.Label(form, text="Type:", font=("Segoe UI", 12), bg="#F2F6FC").grid(row=0, column=2, padx=10)
        self.type_var = ttk.Combobox(form, values=["Expense", "Income"], width=12)
        self.type_var.grid(row=0, column=3, padx=5)

        tk.Label(form, text="Category:", font=("Segoe UI", 12), bg="#F2F6FC").grid(row=0, column=4, padx=10)
        self.cat_var = ttk.Combobox(form, values=self.categories, width=15)
        self.cat_var.grid(row=0, column=5, padx=5)

        tk.Label(form, text="Amount:", font=("Segoe UI", 12), bg="#F2F6FC").grid(row=1, column=0, padx=10, pady=10)
        self.amt_entry = tk.Entry(form, width=15)
        self.amt_entry.grid(row=1, column=1, padx=5)

        tk.Label(form, text="Description:", font=("Segoe UI", 12), bg="#F2F6FC").grid(row=1, column=2, padx=10)
        self.desc_entry = tk.Entry(form, width=20)
        self.desc_entry.grid(row=1, column=3, padx=5)

        tk.Button(form, text="Add", font=("Segoe UI", 12), bg="#00C9FF", fg="white", command=self.add_record).grid(row=1, column=5, padx=10)

        # Treeview
        self.tree = ttk.Treeview(self.root, columns=("Date", "Type", "Category", "Amount", "Description"), show="headings", height=12)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)
        self.tree.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#F2F6FC")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Set Budget", font=("Segoe UI", 10), bg="#00C9FF", fg="white", command=self.set_budget).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Chart Analysis", font=("Segoe UI", 10), bg="#00C9FF", fg="white", command=self.show_charts).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Show View", font=("Segoe UI", 10), bg="#00C9FF", fg="white", command=self.show_view).grid(row=0, column=2, padx=10)
        tk.Button(btn_frame, text="Calendar View", font=("Segoe UI", 10), bg="#00C9FF", fg="white", command=self.calendar_view).grid(row=0, column=3, padx=10)
        tk.Button(btn_frame, text="AI Suggestion", font=("Segoe UI", 10), bg="#00C9FF", fg="white", command=self.ai_suggestion).grid(row=0, column=4, padx=10)
        tk.Button(btn_frame, text="Report Generator", font=("Segoe UI", 10), bg="#00C9FF", fg="white", command=self.generate_report).grid(row=0, column=5, padx=10)
        tk.Button(btn_frame, text="Dark/Light Mode", font=("Segoe UI", 10), bg="#00C9FF", fg="white", command=self.toggle_theme).grid(row=0, column=6, padx=10)

        # Summary
        self.summary = tk.Label(self.root, text="", font=("Segoe UI", 12, "bold"), bg="#F2F6FC", fg="#333")
        self.summary.pack(pady=10)

        self.update_summary()

    def add_record(self):
        date = self.date_entry.get()
        typ = self.type_var.get()
        cat = self.cat_var.get()
        amt = self.amt_entry.get()
        desc = self.desc_entry.get()

        if not all([date, typ, cat, amt]):
            messagebox.showerror("Error", "Fill all fields.")
            return

        try:
            amt = float(amt)
        except:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        self.data.append([date, typ, cat, amt, desc])
        self.tree.insert('', 'end', values=[date, typ, cat, amt, desc])
        self.save_data()
        self.update_summary()

    def update_summary(self):
        exp = sum(x[3] for x in self.data if x[1]=="Expense")
        inc = sum(x[3] for x in self.data if x[1]=="Income")
        bal = inc - exp
        text = f"💸 Expense: ₹{exp}   💰 Income: ₹{inc}   🧮 Balance: ₹{bal}   🎯 Budget: ₹{self.budget}"
        self.summary.config(text=text)

    def set_budget(self):
        def save():
            try:
                self.budget = float(entry.get())
                top.destroy()
                self.update_summary()
            except:
                messagebox.showerror("Error", "Invalid amount.")

        top = tk.Toplevel(self.root)
        top.title("Set Budget")
        entry = tk.Entry(top)
        entry.pack(pady=10)
        tk.Button(top, text="Save", command=save).pack()

    def show_charts(self):
        if not self.data:
            messagebox.showinfo("Info", "No data to show.")
            return

        df = pd.DataFrame(self.data, columns=["Date", "Type", "Category", "Amount", "Description"])
        df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%y")

        win = tk.Toplevel(self.root)
        win.title("Chart Dashboard")

        options = ["Pie", "Donut", "Bar", "Line", "Stacked", "Area"]
        var = tk.StringVar()
        var.set("Pie")

        opt_frame = tk.Frame(win)
        opt_frame.pack()

        for opt in options:
            tk.Radiobutton(opt_frame, text=opt, variable=var, value=opt).pack(side="left", padx=5)

        def plot():
            fig, ax = plt.subplots(figsize=(6,5))
            grp = df.groupby("Category")["Amount"].sum()

            if var.get()=="Pie":
                grp.plot.pie(autopct="%1.1f%%", ax=ax)
            elif var.get()=="Donut":
                wedges, texts, autotexts = ax.pie(grp, autopct='%1.1f%%')
                circle = plt.Circle((0,0), 0.6, color='white')
                ax.add_artist(circle)
            elif var.get()=="Bar":
                grp.plot.bar(color="skyblue", ax=ax)
            elif var.get()=="Line":
                grp.plot.line(marker="o", ax=ax)
            elif var.get()=="Stacked":
                df.pivot_table(index="Date", columns="Category", values="Amount", aggfunc="sum").fillna(0).plot(kind="bar", stacked=True, ax=ax)
            elif var.get()=="Area":
                df.pivot_table(index="Date", columns="Category", values="Amount", aggfunc="sum").fillna(0).plot.area(ax=ax)

            canvas = FigureCanvasTkAgg(fig, master=win)
            canvas.draw()
            canvas.get_tk_widget().pack()

        tk.Button(win, text="Show Chart", command=plot).pack(pady=10)

    def show_view(self):
        win = tk.Toplevel(self.root)
        win.title("All Transactions")

        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=["Date","Type","Category","Amount","Description"], show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=vsb.set)

        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        for row in self.data:
            tree.insert('', 'end', values=row)

    def calendar_view(self):
        win = tk.Toplevel(self.root)
        win.title("Calendar View")
        cal = Calendar(win, selectmode="day")
        cal.pack(pady=10)

    def ai_suggestion(self):
        tips = [
            "Try reducing unnecessary subscriptions.",
            "Track daily expenses for a week.",
            "Use cash for better control.",
            "Review your spending weekly.",
            "Plan meals to avoid food waste."
        ]
        messagebox.showinfo("AI Suggestion", random.choice(tips))

    def generate_report(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path:
            df = pd.DataFrame(self.data, columns=["Date", "Type", "Category", "Amount", "Description"])
            df.to_csv(path, index=False)
            messagebox.showinfo("Report", "Report saved successfully!")

    def toggle_theme(self):
        if not self.dark_mode:
            self.root.config(bg="#2C2F33")
            self.summary.config(bg="#2C2F33", fg="white")
        else:
            self.root.config(bg="#F2F6FC")
            self.summary.config(bg="#F2F6FC", fg="#333")
        self.dark_mode = not self.dark_mode

    def save_data(self):
        df = pd.DataFrame(self.data, columns=["Date", "Type", "Category", "Amount", "Description"])
        df.to_csv("extreme_tracker.csv", index=False)

    def load_data(self):
        if os.path.exists("extreme_tracker.csv"):
            df = pd.read_csv("extreme_tracker.csv")
            self.data = df.values.tolist()
            for row in self.data:
                self.tree.insert('', 'end', values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernExpenseTracker(root)
    root.mainloop()
