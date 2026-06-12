import tkinter as tk
from tkinter import messagebox, ttk
from system_manager import BloodBankManagementSystem
from utils import (
    InvalidDonorIDException, 
    BloodStockNotAvailableException, 
    DuplicateDonorRegistrationException
)

class BloodBankGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Bank Management System")
        self.root.geometry("750x600")
        self.root.configure(bg="#f5f5f5")
        
        self.bbms = BloodBankManagementSystem()
        self.bbms.load_state()
        
        header = tk.Label(root, text="🔴 BLOOD BANK MANAGEMENT SYSTEM 🔴", font=("Arial", 18, "bold"), bg="#d9534f", fg="white", pady=15)
        header.pack(fill=tk.X)
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_donor_tab()
        self.create_donation_tab()
        self.create_request_tab()
        self.create_inventory_tab()
        
        footer_frame = tk.Frame(root, bg="#f5f5f5")
        footer_frame.pack(fill=tk.X, padx=10, pady=10)
        
        save_btn = tk.Button(footer_frame, text="💾 Save Data", command=self.save_data, bg="#5cb85c", fg="white", font=("Arial", 10, "bold"), padx=10)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        export_btn = tk.Button(footer_frame, text="📊 Export CSV Report", command=self.export_csv, bg="#0275d8", fg="white", font=("Arial", 10, "bold"), padx=10)
        export_btn.pack(side=tk.LEFT, padx=5)

    def create_donor_tab(self):
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text="👤 Donor Management")
        
        tk.Label(tab, text="Register New Donor", font=("Arial", 12, "bold"), bg="white", fg="#333").grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="w")
        
        labels = ["Donor ID:", "Name:", "Age:", "Gender:", "Mobile:", "Blood Group:"]
        self.donor_entries = {}
        
        for i, label_text in enumerate(labels):
            tk.Label(tab, text=label_text, bg="white", font=("Arial", 10)).grid(row=i+1, column=0, padx=15, pady=5, sticky="e")
            entry = tk.Entry(tab, font=("Arial", 10), width=30)
            entry.grid(row=i+1, column=1, padx=15, pady=5, sticky="w")
            self.donor_entries[label_text] = entry
            
        reg_btn = tk.Button(tab, text="Register Donor", command=self.register_donor, bg="#d9534f", fg="white", font=("Arial", 10, "bold"))
        reg_btn.grid(row=8, column=1, pady=15, sticky="w")

    def create_donation_tab(self):
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text="🩸 Record Donation")
        
        tk.Label(tab, text="Log Blood Donation", font=("Arial", 12, "bold"), bg="white", fg="#333").grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="w")
        
        tk.Label(tab, text="Donor ID:", bg="white").grid(row=1, column=0, padx=15, pady=10, sticky="e")
        self.don_id_entry = tk.Entry(tab, width=30)
        self.don_id_entry.grid(row=1, column=1, padx=15, pady=10)
        
        tk.Label(tab, text="Quantity (ml):", bg="white").grid(row=2, column=0, padx=15, pady=10, sticky="e")
        self.don_qty_entry = tk.Entry(tab, width=30)
        self.don_qty_entry.grid(row=2, column=1, padx=15, pady=10)
        
        don_btn = tk.Button(tab, text="Record Donation", command=self.record_donation, bg="#5bc0de", fg="white", font=("Arial", 10, "bold"))
        don_btn.grid(row=3, column=1, pady=15, sticky="w")

    def create_request_tab(self):
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text="🏥 Hospital Request")
        
        tk.Label(tab, text="Process Hospital Blood Request", font=("Arial", 12, "bold"), bg="white", fg="#333").grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="w")
        
        tk.Label(tab, text="Hospital Name:", bg="white").grid(row=1, column=0, padx=15, pady=10, sticky="e")
        self.req_hosp_entry = tk.Entry(tab, width=30)
        self.req_hosp_entry.grid(row=1, column=1, padx=15, pady=10)
        
        tk.Label(tab, text="Blood Group:", bg="white").grid(row=2, column=0, padx=15, pady=10, sticky="e")
        self.req_bg_entry = tk.Entry(tab, width=30)
        self.req_bg_entry.grid(row=2, column=1, padx=15, pady=10)
        
        tk.Label(tab, text="Quantity Needed (ml):", bg="white").grid(row=3, column=0, padx=15, pady=10, sticky="e")
        self.req_qty_entry = tk.Entry(tab, width=30)
        self.req_qty_entry.grid(row=3, column=1, padx=15, pady=10)
        
        req_btn = tk.Button(tab, text="Process Request", command=self.process_request, bg="#f0ad4e", fg="white", font=("Arial", 10, "bold"))
        req_btn.grid(row=4, column=1, pady=15, sticky="w")

    def create_inventory_tab(self):
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text="📊 View Inventory")
        
        refresh_btn = tk.Button(tab, text="🔄 Refresh Stock View", command=self.refresh_inventory, bg="#337ab7", fg="white")
        refresh_btn.pack(anchor="nw", padx=10, pady=10)
        
        columns = ("unit_id", "bg", "qty", "expiry")
        self.tree = ttk.Treeview(tab, columns=columns, show="headings", height=15)
        
        self.tree.heading("unit_id", text="Unit ID")
        self.tree.heading("bg", text="Blood Group")
        self.tree.heading("qty", text="Quantity (ml)")
        self.tree.heading("expiry", text="Expiry Date")
        
        self.tree.column("unit_id", width=100)
        self.tree.column("bg", width=120)
        self.tree.column("qty", width=120)
        self.tree.column("expiry", width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.refresh_inventory()
    
    def register_donor(self):
        try:
            d_id = self.donor_entries["Donor ID:"].get().strip()
            name = self.donor_entries["Name:"].get().strip()
            age = int(self.donor_entries["Age:"].get().strip())
            gender = self.donor_entries["Gender:"].get().strip()
            mob = self.donor_entries["Mobile:"].get().strip()
            bg = self.donor_entries["Blood Group:"].get().strip().upper()
            
            if not d_id or not name or not bg:
                raise ValueError("Fields cannot be empty!")
                
            self.bbms.register_donor(d_id, name, age, gender, mob, bg)
            messagebox.showinfo("Success", f"Donor {name} registered successfully!")
            
            for entry in self.donor_entries.values(): entry.delete(0, tk.END)
        except DuplicateDonorRegistrationException as e:
            messagebox.showerror("Error", str(e))
        except ValueError:
            messagebox.showerror("Input Error", "Please fill valid details and correct numeric values for Age.")

    def record_donation(self):
        try:
            d_id = self.don_id_entry.get().strip()
            qty = float(self.don_qty_entry.get().strip())
            
            success = self.bbms.record_donation(d_id, qty)
            if success:
                messagebox.showinfo("Success", "Blood donation recorded successfully into stock!")
                self.don_id_entry.delete(0, tk.END)
                self.don_qty_entry.delete(0, tk.END)
                self.refresh_inventory()
            else:
                messagebox.showwarning("Ineligible", "Donor is not eligible for donation currently.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def process_request(self):
        try:
            hosp = self.req_hosp_entry.get().strip()
            bg = self.req_bg_entry.get().strip().upper()
            qty = float(self.req_qty_entry.get().strip())
            
            req_id = f"REQ-{len(self.bbms.blood_requests) + 1}"
            self.bbms.process_request(req_id, hosp, bg, qty)
            
            messagebox.showinfo("Approved", "Blood request approved! Units allocated successfully.")
            self.refresh_inventory()
        except BloodStockNotAvailableException as e:
            messagebox.showwarning("Stock Alert", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_inventory(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for unit in self.bbms.blood_report_generator():
            self.tree.insert("", tk.END, values=(unit["Unit ID"], unit["Group"], unit["Qty"], unit["Expiry"]))

    def save_data(self):
        self.bbms.save_state()
        messagebox.showinfo("Saved", "Database state saved successfully to JSON.")

    def export_csv(self):
        self.bbms.export_stock_to_csv()
        messagebox.showinfo("Exported", "Inventory report exported to 'data/stock_report.csv'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BloodBankGUI(root)
    root.mainloop()