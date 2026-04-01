import tkinter as tk
from tkinter import messagebox, ttk
import hashlib
import random
import json
from datetime import datetime

# ─── In-memory database ───────────────────────────────────────────────────────
users = {}
current_user = [None]

# ─── Colors & Fonts ───────────────────────────────────────────────────────────
BG        = "#0D1117"
CARD      = "#161B22"
ACCENT    = "#00C896"
ACCENT2   = "#0077FF"
TEXT      = "#E6EDF3"
MUTED     = "#8B949E"
DANGER    = "#FF4C4C"
WARN      = "#FFA500"
BORDER    = "#30363D"

FONT_H1   = ("Georgia", 22, "bold")
FONT_H2   = ("Georgia", 16, "bold")
FONT_BODY = ("Courier", 13)
FONT_SM   = ("Courier", 11)
FONT_BTN  = ("Georgia", 13, "bold")

# ─── Core Logic ───────────────────────────────────────────────────────────────
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def gen_acc():
    while True:
        acc = str(random.randint(1000000000, 9999999999))
        if acc not in users:
            return acc

def add_txn(acc, txn_type, amount, note=""):
    entry = {
        "type": txn_type,
        "amount": amount,
        "note": note,
        "time": datetime.now().strftime("%d %b %Y  %H:%M")
    }
    users[acc]["transactions"].append(entry)

def create_account(name, aadhaar, mobile, password):
    name, aadhaar, mobile = name.strip(), aadhaar.strip(), mobile.strip()
    if not name:
        return None, "Name cannot be empty."
    if len(aadhaar) != 12 or not aadhaar.isdigit():
        return None, "Aadhaar must be exactly 12 digits."
    if len(mobile) != 10 or not mobile.isdigit():
        return None, "Mobile must be exactly 10 digits."
    if len(password) < 8:
        return None, "Password must be at least 8 characters."
    for u in users.values():
        if u["aadhaar"] == aadhaar:
            return None, "Aadhaar already registered."
    acc = gen_acc()
    users[acc] = {
        "name": name,
        "aadhaar": aadhaar,
        "mobile": mobile,
        "password_hash": hash_pw(password),
        "balance": 0.0,
        "transactions": []
    }
    return acc, f"Account created successfully!\nYour Account Number: {acc}"

def login(acc, pw):
    if acc not in users:
        return False, "Account not found."
    if users[acc]["password_hash"] != hash_pw(pw):
        return False, "Incorrect password."
    current_user[0] = acc
    return True, f"Welcome back, {users[acc]['name']}!"

def logout():
    current_user[0] = None

def deposit(amount):
    try:
        amt = float(amount)
        if amt <= 0:
            return "Amount must be positive."
        users[current_user[0]]["balance"] += amt
        add_txn(current_user[0], "Credit", amt, "Deposit")
        return f"₹{amt:,.2f} deposited successfully."
    except ValueError:
        return "Invalid amount."

def withdraw(amount):
    try:
        amt = float(amount)
        if amt <= 0:
            return "Amount must be positive."
        if users[current_user[0]]["balance"] < amt:
            return "Insufficient balance."
        users[current_user[0]]["balance"] -= amt
        add_txn(current_user[0], "Debit", amt, "Withdrawal")
        return f"₹{amt:,.2f} withdrawn successfully."
    except ValueError:
        return "Invalid amount."

def transfer(to_acc, amount):
    try:
        amt = float(amount)
        if amt <= 0:
            return "Amount must be positive."
        if to_acc == current_user[0]:
            return "Cannot transfer to own account."
        if to_acc not in users:
            return "Recipient account not found."
        if users[current_user[0]]["balance"] < amt:
            return "Insufficient balance."
        users[current_user[0]]["balance"] -= amt
        users[to_acc]["balance"] += amt
        rname = users[to_acc]["name"]
        add_txn(current_user[0], "Debit",  amt, f"Transfer to {rname}")
        add_txn(to_acc,          "Credit", amt, f"Transfer from {users[current_user[0]]['name']}")
        return f"₹{amt:,.2f} transferred to {rname} ({to_acc})."
    except ValueError:
        return "Invalid amount."

def get_balance():
    return users[current_user[0]]["balance"]

def get_mini_statement():
    txns = users[current_user[0]]["transactions"]
    return txns[-5:][::-1] if txns else []

# ─── GUI ──────────────────────────────────────────────────────────────────────
def run():
    root = tk.Tk()
    root.title("Cosmos Bank")
    root.configure(bg=BG)
    root.geometry("900x650")
    root.resizable(False, False)

    # ── helpers ──────────────────────────────────────────────────────────────
    def clr():
        for w in root.winfo_children():
            w.destroy()

    def lbl(parent, text, font=FONT_BODY, color=TEXT, bg=BG, anchor="w", **kw):
        return tk.Label(parent, text=text, font=font, fg=color, bg=bg,
                        anchor=anchor, **kw)

    def entry(parent, show=None):
        e = tk.Entry(parent, font=FONT_BODY, fg=TEXT, bg=CARD,
                     insertbackground=ACCENT, relief="flat",
                     highlightthickness=1, highlightcolor=ACCENT,
                     highlightbackground=BORDER, show=show or "")
        e.config(width=30)
        return e

    def btn(parent, text, cmd, color=ACCENT, fg=BG, width=22):
        return tk.Button(parent, text=text, command=cmd,
                         font=FONT_BTN, fg=fg, bg=color,
                         activebackground=color, activeforeground=fg,
                         relief="flat", cursor="hand2", width=width,
                         padx=6, pady=6)

    def separator(parent, bg=BORDER):
        return tk.Frame(parent, bg=bg, height=1)

    def toast(msg, color=ACCENT):
        t = tk.Toplevel(root)
        t.overrideredirect(True)
        t.configure(bg=CARD)
        t.attributes("-topmost", True)
        rx, ry = root.winfo_x(), root.winfo_y()
        t.geometry(f"400x46+{rx+250}+{ry+590}")
        tk.Label(t, text=msg, font=FONT_SM, fg=color, bg=CARD,
                 padx=12, pady=10).pack(fill="both")
        t.after(2500, t.destroy)

    # ── Login Screen ─────────────────────────────────────────────────────────
    def show_login():
        clr()

        # Header bar
        bar = tk.Frame(root, bg=CARD, height=56)
        bar.pack(fill="x")
        lbl(bar, "  🏦  COSMOS BANK", FONT_H1, ACCENT, CARD).pack(side="left", pady=10, padx=10)
        lbl(bar, "Trusted · Secure · Simple", FONT_SM, MUTED, CARD).pack(side="right", padx=20)

        # Center card
        wrap = tk.Frame(root, bg=BG)
        wrap.pack(expand=True)

        card = tk.Frame(wrap, bg=CARD, padx=40, pady=30,
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(pady=30)

        lbl(card, "Sign In to Your Account", FONT_H2, TEXT, CARD).pack(anchor="w", pady=(0, 20))

        lbl(card, "Account Number", FONT_SM, MUTED, CARD).pack(anchor="w")
        acc_e = entry(card); acc_e.pack(fill="x", pady=(2, 10), ipady=6)

        lbl(card, "Password", FONT_SM, MUTED, CARD).pack(anchor="w")
        pw_e = entry(card, show="*"); pw_e.pack(fill="x", pady=(2, 16), ipady=6)

        def do_login():
            ok, msg = login(acc_e.get().strip(), pw_e.get())
            if ok:
                show_dashboard()
            else:
                toast(msg, DANGER)

        btn(card, "LOGIN  →", do_login).pack(fill="x", pady=(4, 10))
        separator(card).pack(fill="x", pady=10)
        btn(card, "Create New Account", show_register,
            color=CARD, fg=ACCENT, width=22).pack(fill="x")

        # bind Enter key
        root.bind("<Return>", lambda e: do_login())

    # ── Register Screen ───────────────────────────────────────────────────────
    def show_register():
        clr()
        root.unbind("<Return>")

        bar = tk.Frame(root, bg=CARD, height=56)
        bar.pack(fill="x")
        lbl(bar, "  🏦  COSMOS BANK", FONT_H1, ACCENT, CARD).pack(side="left", pady=10, padx=10)

        wrap = tk.Frame(root, bg=BG)
        wrap.pack(expand=True)

        card = tk.Frame(wrap, bg=CARD, padx=40, pady=25,
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(pady=20)

        lbl(card, "Open a New Account", FONT_H2, TEXT, CARD).pack(anchor="w", pady=(0, 18))

        fields = {}
        specs = [
            ("Full Name",          "name",     None),
            ("Aadhaar Number (12 digits)", "aadhaar", None),
            ("Mobile Number (10 digits)",  "mobile",  None),
            ("Password (min 8 chars)",     "pw",      "*"),
            ("Confirm Password",           "cpw",     "*"),
        ]
        for label_text, key, show in specs:
            lbl(card, label_text, FONT_SM, MUTED, CARD).pack(anchor="w")
            e = entry(card, show=show)
            e.pack(fill="x", pady=(2, 8), ipady=6)
            fields[key] = e

        def do_register():
            if fields["pw"].get() != fields["cpw"].get():
                toast("Passwords do not match.", DANGER); return
            acc, msg = create_account(
                fields["name"].get(), fields["aadhaar"].get(),
                fields["mobile"].get(), fields["pw"].get()
            )
            if acc:
                show_success(acc)
            else:
                toast(msg, DANGER)

        btn(card, "CREATE ACCOUNT  →", do_register).pack(fill="x", pady=(6, 6))
        btn(card, "← Back to Login", show_login, color=CARD, fg=MUTED).pack(fill="x")

    # ── Success Screen ────────────────────────────────────────────────────────
    def show_success(acc):
        clr()

        bar = tk.Frame(root, bg=CARD, height=56)
        bar.pack(fill="x")
        lbl(bar, "  🏦  COSMOS BANK", FONT_H1, ACCENT, CARD).pack(side="left", pady=10, padx=10)

        wrap = tk.Frame(root, bg=BG)
        wrap.pack(expand=True)

        card = tk.Frame(wrap, bg=CARD, padx=50, pady=40,
                        highlightthickness=1, highlightbackground=ACCENT)
        card.pack(pady=30)

        lbl(card, "✅  Account Created!", FONT_H1, ACCENT, CARD).pack(pady=(0, 10))
        lbl(card, "Save your Account Number carefully.", FONT_SM, MUTED, CARD).pack()

        lbl(card, "", bg=CARD).pack()
        lbl(card, "Your Account Number", FONT_SM, MUTED, CARD).pack()
        acc_var = tk.StringVar(value=acc)
        acc_disp = tk.Entry(card, textvariable=acc_var, font=("Courier", 20, "bold"),
                            fg=ACCENT, bg=BG, justify="center", state="readonly",
                            relief="flat", readonlybackground=BG)
        acc_disp.pack(pady=8, ipady=8, fill="x")

        def copy():
            root.clipboard_clear()
            root.clipboard_append(acc)
            toast("Account number copied to clipboard!", ACCENT)

        btn(card, "📋  Copy Account Number", copy, color=ACCENT2, fg=TEXT).pack(fill="x", pady=6)
        btn(card, "Go to Login  →", show_login).pack(fill="x")

    # ── Dashboard ─────────────────────────────────────────────────────────────
    def show_dashboard():
        clr()
        root.unbind("<Return>")
        acc  = current_user[0]
        user = users[acc]

        # ── Top bar ──────────────────────────────────────────────────────────
        bar = tk.Frame(root, bg=CARD, height=52)
        bar.pack(fill="x")
        lbl(bar, "  🏦  COSMOS BANK", FONT_H1, ACCENT, CARD).pack(side="left", pady=8, padx=10)

        def do_logout():
            logout()
            show_login()

        btn(bar, "Logout", do_logout, color=DANGER, fg=TEXT, width=10).pack(
            side="right", padx=14, pady=8)
        lbl(bar, f"👤 {user['name']}  |  A/C: {acc}", FONT_SM, MUTED, CARD).pack(
            side="right", pady=12)

        # ── Body ─────────────────────────────────────────────────────────────
        body = tk.Frame(root, bg=BG)
        body.pack(fill="both", expand=True, padx=20, pady=16)

        left  = tk.Frame(body, bg=BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = tk.Frame(body, bg=BG, width=280)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        # ── Balance card ─────────────────────────────────────────────────────
        bal_card = tk.Frame(left, bg=CARD, padx=20, pady=16,
                            highlightthickness=1, highlightbackground=ACCENT)
        bal_card.pack(fill="x", pady=(0, 14))

        lbl(bal_card, "Available Balance", FONT_SM, MUTED, CARD).pack(anchor="w")
        bal_var = tk.StringVar(value=f"₹{get_balance():,.2f}")
        lbl(bal_card, "", FONT_SM, MUTED, CARD, textvariable=bal_var).pack(anchor="w")  # placeholder replaced below
        bal_lbl = tk.Label(bal_card, textvariable=bal_var,
                           font=("Georgia", 28, "bold"), fg=ACCENT, bg=CARD)
        bal_lbl.pack(anchor="w")

        def refresh_bal():
            bal_var.set(f"₹{get_balance():,.2f}")
            refresh_stmt()

        # ── Tabs ─────────────────────────────────────────────────────────────
        tab_frame = tk.Frame(left, bg=BG)
        tab_frame.pack(fill="x", pady=(0, 8))

        panels = {}
        active_tab = [None]

        tab_names = ["Deposit", "Withdraw", "Transfer"]
        tab_btns   = {}

        def show_tab(name):
            for n, p in panels.items():
                p.pack_forget()
            panels[name].pack(fill="x")
            for n, b in tab_btns.items():
                b.config(bg=CARD if n != name else ACCENT,
                         fg=TEXT  if n != name else BG)
            active_tab[0] = name

        for tname in tab_names:
            b = tk.Button(tab_frame, text=tname, font=FONT_BTN, fg=TEXT,
                          bg=CARD, activebackground=ACCENT, activeforeground=BG,
                          relief="flat", cursor="hand2", padx=16, pady=6,
                          command=lambda n=tname: show_tab(n))
            b.pack(side="left", padx=(0, 4))
            tab_btns[tname] = b

        # ── Deposit panel ────────────────────────────────────────────────────
        dep_panel = tk.Frame(left, bg=CARD, padx=20, pady=16,
                             highlightthickness=1, highlightbackground=BORDER)
        panels["Deposit"] = dep_panel

        lbl(dep_panel, "Amount to Deposit (₹)", FONT_SM, MUTED, CARD).pack(anchor="w")
        dep_e = entry(dep_panel); dep_e.pack(fill="x", pady=(4, 10), ipady=6)

        def do_dep():
            msg = deposit(dep_e.get())
            dep_e.delete(0, "end")
            refresh_bal()
            toast(msg, ACCENT if "successfully" in msg else DANGER)

        btn(dep_panel, "Deposit  →", do_dep).pack(anchor="w")

        # ── Withdraw panel ───────────────────────────────────────────────────
        wd_panel = tk.Frame(left, bg=CARD, padx=20, pady=16,
                            highlightthickness=1, highlightbackground=BORDER)
        panels["Withdraw"] = wd_panel

        lbl(wd_panel, "Amount to Withdraw (₹)", FONT_SM, MUTED, CARD).pack(anchor="w")
        wd_e = entry(wd_panel); wd_e.pack(fill="x", pady=(4, 10), ipady=6)

        def do_wd():
            msg = withdraw(wd_e.get())
            wd_e.delete(0, "end")
            refresh_bal()
            toast(msg, ACCENT if "successfully" in msg else DANGER)

        btn(wd_panel, "Withdraw  →", do_wd, color=WARN, fg=BG).pack(anchor="w")

        # ── Transfer panel ───────────────────────────────────────────────────
        tr_panel = tk.Frame(left, bg=CARD, padx=20, pady=16,
                            highlightthickness=1, highlightbackground=BORDER)
        panels["Transfer"] = tr_panel

        lbl(tr_panel, "Recipient Account Number", FONT_SM, MUTED, CARD).pack(anchor="w")
        tr_acc_e = entry(tr_panel); tr_acc_e.pack(fill="x", pady=(4, 8), ipady=6)
        lbl(tr_panel, "Amount (₹)", FONT_SM, MUTED, CARD).pack(anchor="w")
        tr_amt_e = entry(tr_panel); tr_amt_e.pack(fill="x", pady=(4, 10), ipady=6)

        def do_tr():
            msg = transfer(tr_acc_e.get().strip(), tr_amt_e.get())
            tr_acc_e.delete(0, "end")
            tr_amt_e.delete(0, "end")
            refresh_bal()
            toast(msg, ACCENT if "transferred" in msg else DANGER)

        btn(tr_panel, "Transfer  →", do_tr, color=ACCENT2, fg=TEXT).pack(anchor="w")

        show_tab("Deposit")

        # ── Right panel: Mini Statement ───────────────────────────────────────
        stmt_card = tk.Frame(right, bg=CARD, padx=14, pady=14,
                             highlightthickness=1, highlightbackground=BORDER)
        stmt_card.pack(fill="both", expand=True)

        lbl(stmt_card, "Recent Transactions", FONT_SM, ACCENT, CARD).pack(anchor="w", pady=(0, 8))
        separator(stmt_card).pack(fill="x", pady=(0, 8))

        stmt_body = tk.Frame(stmt_card, bg=CARD)
        stmt_body.pack(fill="both", expand=True)

        def refresh_stmt():
            for w in stmt_body.winfo_children():
                w.destroy()
            txns = get_mini_statement()
            if not txns:
                lbl(stmt_body, "No transactions yet.", FONT_SM, MUTED, CARD).pack(anchor="w")
                return
            for t in txns:
                color = ACCENT if t["type"] == "Credit" else DANGER
                sign  = "+" if t["type"] == "Credit" else "-"
                row = tk.Frame(stmt_body, bg=CARD)
                row.pack(fill="x", pady=3)
                tk.Label(row, text=t["note"], font=FONT_SM, fg=TEXT,
                         bg=CARD, anchor="w", width=18).pack(side="left")
                tk.Label(row, text=f"{sign}₹{t['amount']:,.0f}",
                         font=("Courier", 11, "bold"), fg=color,
                         bg=CARD, anchor="e").pack(side="right")
                tk.Label(stmt_body, text=t["time"], font=("Courier", 9),
                         fg=MUTED, bg=CARD, anchor="w").pack(fill="x")
                tk.Frame(stmt_body, bg=BORDER, height=1).pack(fill="x", pady=2)

        refresh_stmt()

    show_login()
    root.mainloop()

if __name__ == "__main__":
    run()
