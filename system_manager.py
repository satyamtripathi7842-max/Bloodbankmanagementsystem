import json
import csv
import os
from models import Donor, BloodUnit, BloodRequest, BloodCamp
from utils import log_action, InvalidDonorIDException, DuplicateDonorRegistrationException, BloodStockNotAvailableException

class BloodBankManagementSystem:
    def __init__(self):
        self.donors = {}              
        self.blood_units = []         
        self.blood_requests = []      
        self.blood_camps = []         
        self.hospitals = {}           
        self.donations_log = []       
        
    def __len__(self):
        return len(self.blood_units)

    # Recursive Function to search donor records
    def search_donor_recursive(self, donor_ids_list, target_id, index=0):
        if index >= len(donor_ids_list):
            return None
        if donor_ids_list[index] == target_id:
            return self.donors[target_id]
        return self.search_donor_recursive(donor_ids_list, target_id, index + 1)

    @log_action("Donor Registration")
    def register_donor(self, donor_id, name, age, gender, mobile_number, blood_group):
        if donor_id in self.donors:
            raise DuplicateDonorRegistrationException(f"Donor ID {donor_id} already exists!")
        
        new_donor = Donor(donor_id, name, age, gender, mobile_number, blood_group)
        self.donors[donor_id] = new_donor
        return new_donor

    @log_action("Blood Donation Logged")
    def record_donation(self, donor_id, quantity, expiry_days=35):
        if donor_id not in self.donors:
            raise InvalidDonorIDException("Donor not registered!")
        
        donor_obj = self.donors[donor_id]
        if not donor_obj.check_eligibility():
            print("⚠️ Donor is currently NOT eligible to donate.")
            return False
            
        from datetime import datetime, timedelta
        today_str = datetime.now().strftime("%Y-%m-%d")
        exp_str = (datetime.now() + timedelta(days=expiry_days)).strftime("%Y-%m-%d")
        
        donor_obj.donate_blood(quantity, today_str)
        
        unit_id = f"UNIT-{len(self.blood_units) + 101}"
        new_unit = BloodUnit(unit_id, donor_obj.blood_group, quantity, today_str, exp_str)
        self.blood_units.append(new_unit)
        
        self.donations_log.append({
            "donation_id": f"DON-{len(self.donations_log) + 1}",
            "donor_id": donor_id,
            "date": today_str,
            "quantity": quantity
        })
        return True

    @log_action("Blood Allocation")
    def process_request(self, request_id, hospital_name, blood_group, required_qty):
        req = BloodRequest(request_id, hospital_name, blood_group, required_qty)
        self.blood_requests.append(req)
        
        # List Comprehension used to filter blood units
        available_units = [u for u in self.blood_units if u.blood_group == blood_group and not u.check_expiry()]
        total_available = sum(u.quantity for u in available_units)
        
        if total_available < required_qty:
            req.reject_request()
            raise BloodStockNotAvailableException(f"Required: {required_qty}ml, Available: {total_available}ml for group {blood_group}")
        
        allocated = 0
        units_to_keep = []
        for u in self.blood_units:
            if u.blood_group == blood_group and not u.check_expiry() and allocated < required_qty:
                needed = required_qty - allocated
                if u.quantity <= needed:
                    allocated += u.quantity
                else:
                    u.quantity -= needed
                    allocated += needed
                    units_to_keep.append(u)
            else:
                units_to_keep.append(u)
                
        self.blood_units = units_to_keep
        req.approve_request()
        return True

    # Generator used to yield records one at a time
    def blood_report_generator(self):
        for unit in self.blood_units:
            yield {"Unit ID": unit.unit_id, "Group": unit.blood_group, "Qty": unit.quantity, "Expiry": unit.expiry_date}

    # JSON File Handling
    def save_state(self, folder="data"):
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        state_data = {
            "donors": {k: v.__dict__ for k, v in self.donors.items()},
            "units": [u.__dict__ for u in self.blood_units],
            "requests": [r.__dict__ for r in self.blood_requests],
            "donations": self.donations_log
        }
        with open(f"{folder}/blood_bank_data.json", "w") as f:
            json.dump(state_data, f, indent=4)
        print("💾 All data saved to JSON successfully.")

    def load_state(self, folder="data"):
        filepath = f"{folder}/blood_bank_data.json"
        if not os.path.exists(filepath):
            print("ℹ️ No previous database file found. Starting fresh.")
            return
            
        with open(filepath, "r") as f:
            data = json.load(f)
            
        for k, v in data.get("donors", {}).items():
            donor = Donor(v['donor_id'], v['name'], v['age'], v['gender'], v['mobile_number'], v['blood_group'], v.get('last_donation_date'), v.get('donation_history'))
            self.donors[k] = donor
            
        for u in data.get("units", []):
            self.blood_units.append(BloodUnit(u['unit_id'], u['blood_group'], u['quantity'], u['collection_date'], u['expiry_date']))
            
        for r in data.get("requests", []):
            self.blood_requests.append(BloodRequest(r['request_id'], r['hospital_name'], r['blood_group'], r['quantity'], r['request_status']))
            
        self.donations_log = data.get("donations", [])
        print("📂 Data loaded successfully from JSON storage.")

    # CSV File Handling
    def export_stock_to_csv(self, filepath="data/stock_report.csv"):
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Unit ID", "Blood Group", "Quantity (ml)", "Expiry Date"])
            for row in self.blood_report_generator():
                writer.writerow([row["Unit ID"], row["Group"], row["Qty"], row["Expiry"]])
        print(f"📊 Report successfully exported to {filepath}")