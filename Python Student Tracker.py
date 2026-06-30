
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date

# ---------- DATABASE ----------
con = sqlite3.connect("student.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS habits(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    target REAL,
    done REAL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS deadlines(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    category TEXT,
    ddate TEXT,
    status TEXT
)
""")
con.commit()

# ---------- APP ----------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Habit & Deadline Tracker")
        self.root.geometry("1300x650")
        self.root.configure(bg="#0f172a")

        self.hid = None
        self.did = None

        self.build_ui()
        self.refresh()

    # ---------- UI ----------
    def build_ui(self):
        tk.Label(self.root, text="Student Habit & Deadline Tracker",
                 bg="#020617", fg="#38bdf8",
                 font=("Segoe UI", 18)).pack(fill="x", pady=6)

        main = tk.Frame(self.root, bg="#0f172a")
        main.pack(fill="both", expand=True, padx=10, pady=8)

        # ========== HABITS ==========
        left = tk.LabelFrame(main, text="Habits",
                             bg="#020617", fg="#22c55e")
        left.pack(side="left", fill="both", expand=True, padx=6)

        form_h = tk.Frame(left, bg="#020617")
        form_h.pack(fill="x", pady=4)

        tk.Label(form_h, text="Habit", bg="#020617", fg="white").grid(row=0, column=0)
        tk.Label(form_h, text="Target", bg="#020617", fg="white").grid(row=0, column=1)
        tk.Label(form_h, text="Done", bg="#020617", fg="white").grid(row=0, column=2)

        self.hname = tk.Entry(form_h, width=20)
        self.htarget = tk.Entry(form_h, width=8)
        self.hdone = tk.Entry(form_h, width=8)

        self.hname.grid(row=1, column=0, padx=4)
        self.htarget.grid(row=1, column=1, padx=4)
        self.hdone.grid(row=1, column=2, padx=4)

        tk.Button(form_h, text="Add Habit", command=self.add_habit)\
            .grid(row=1, column=3, padx=6)

        self.habits = ttk.Treeview(
            left, columns=("id","n","t","d","s"),
            show="headings", height=12)

        for c,h,w in [
            ("id","ID",50),("n","Habit",220),
            ("t","Target",90),("d","Done",90),("s","Status",100)
        ]:
            self.habits.heading(c, text=h)
            self.habits.column(c, width=w, anchor="center")

        self.habits.pack(fill="both", expand=True, pady=8)
        self.habits.bind("<<TreeviewSelect>>", self.load_habit)

        btn_h = tk.Frame(left, bg="#020617")
        btn_h.pack(pady=6)
        tk.Button(btn_h, text="Update", width=12, command=self.update_habit).pack(side="left", padx=6)
        tk.Button(btn_h, text="Delete", width=12, command=self.delete_habit).pack(side="left", padx=6)

        # ========== DEADLINES ==========
        right = tk.LabelFrame(main, text="Deadlines",
                              bg="#020617", fg="#facc15")
        right.pack(side="right", fill="both", expand=True, padx=6)

        form_d = tk.Frame(right, bg="#020617")
        form_d.pack(fill="x", pady=4)

        tk.Label(form_d, text="Title", bg="#020617", fg="white").grid(row=0, column=0)
        tk.Label(form_d, text="Category", bg="#020617", fg="white").grid(row=0, column=1)
        tk.Label(form_d, text="Date", bg="#020617", fg="white").grid(row=0, column=2)

        self.dtitle = tk.Entry(form_d, width=22)
        self.dcat = ttk.Combobox(
            form_d,
            values=["Academic","Personal","Health","Finance","Project","Other"],
            state="readonly", width=16)
        self.dcat.set("Academic")

        self.ddate = tk.Entry(form_d, width=14)
        self.ddate.insert(0, str(date.today()))

        self.dtitle.grid(row=1, column=0, padx=4)
        self.dcat.grid(row=1, column=1, padx=4)
        self.ddate.grid(row=1, column=2, padx=4)

        tk.Button(form_d, text="Add Deadline", command=self.add_deadline)\
            .grid(row=1, column=3, padx=6)

        self.deadlines = ttk.Treeview(
            right, columns=("id","t","c","d","s"),
            show="headings", height=12)

        for c,h,w in [
            ("id","ID",50),("t","Title",240),
            ("c","Category",150),("d","Date",110),("s","Status",110)
        ]:
            self.deadlines.heading(c, text=h)
            self.deadlines.column(c, width=w, anchor="center")

        self.deadlines.pack(fill="both", expand=True, pady=8)
        self.deadlines.bind("<<TreeviewSelect>>", self.load_deadline)

        btn_d = tk.Frame(right, bg="#020617")
        btn_d.pack(pady=6)
        tk.Button(btn_d, text="Update", width=12, command=self.update_deadline).pack(side="left", padx=6)
        tk.Button(btn_d, text="Complete", width=12, command=self.complete_deadline).pack(side="left", padx=6)
        tk.Button(btn_d, text="Delete", width=12, command=self.delete_deadline).pack(side="left", padx=6)

    # ---------- HABITS ----------
    def load_habit(self, _):
        r = self.habits.item(self.habits.focus())["values"]
        if not r: return
        self.hid = r[0]
        self.hname.delete(0,"end")
        self.htarget.delete(0,"end")
        self.hdone.delete(0,"end")
        self.hname.insert(0,r[1])
        self.htarget.insert(0,r[2])
        self.hdone.insert(0,r[3])

    def add_habit(self):
        cur.execute("INSERT INTO habits VALUES(NULL,?,?,?)",
            (self.hname.get(), float(self.htarget.get()), float(self.hdone.get())))
        con.commit()
        self.refresh()

    def update_habit(self):
        if not self.hid:
            messagebox.showwarning("Select", "Select a habit")
            return
        cur.execute("UPDATE habits SET name=?,target=?,done=? WHERE id=?",
            (self.hname.get(), float(self.htarget.get()),
             float(self.hdone.get()), self.hid))
        con.commit()
        self.hid = None
        self.refresh()

    def delete_habit(self):
        r = self.habits.item(self.habits.focus())["values"]
        if r:
            cur.execute("DELETE FROM habits WHERE id=?", (r[0],))
            con.commit()
            self.refresh()

    # ---------- DEADLINES ----------
    def load_deadline(self, _):
        r = self.deadlines.item(self.deadlines.focus())["values"]
        if not r: return
        self.did = r[0]
        self.dtitle.delete(0,"end")
        self.ddate.delete(0,"end")
        self.dtitle.insert(0,r[1])
        self.dcat.set(r[2])
        self.ddate.insert(0,r[3])

    def add_deadline(self):
        cur.execute("INSERT INTO deadlines VALUES(NULL,?,?,?,?)",
            (self.dtitle.get(), self.dcat.get(),
             self.ddate.get(), "Pending"))
        con.commit()
        self.refresh()

    def update_deadline(self):
        if not self.did:
            messagebox.showwarning("Select", "Select a deadline")
            return
        cur.execute("UPDATE deadlines SET title=?,category=?,ddate=? WHERE id=?",
            (self.dtitle.get(), self.dcat.get(), self.ddate.get(), self.did))
        con.commit()
        self.did = None
        self.refresh()

    def complete_deadline(self):
        r = self.deadlines.item(self.deadlines.focus())["values"]
        if r:
            cur.execute("UPDATE deadlines SET status='Completed' WHERE id=?", (r[0],))
            con.commit()
            self.refresh()

    def delete_deadline(self):
        r = self.deadlines.item(self.deadlines.focus())["values"]
        if r:
            cur.execute("DELETE FROM deadlines WHERE id=?", (r[0],))
            con.commit()
            self.refresh()

    # ---------- REFRESH ----------
    def refresh(self):
        for tv in (self.habits, self.deadlines):
            for i in tv.get_children():
                tv.delete(i)

        for h in cur.execute("SELECT * FROM habits"):
            self.habits.insert("", "end",
                values=(*h, "Completed" if h[3]>=h[2] else "Pending"))

        for d in cur.execute("SELECT * FROM deadlines"):
            self.deadlines.insert("", "end", values=d)


# ---------- RUN ----------
root = tk.Tk()
App(root)
root.mainloop()
