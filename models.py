# Custom exception jab blood stock available na ho
class BloodStockNotAvailableException(Exception):
    pass

class BloodBankManagementSystem:
    def __init__(self):
        # Shuruat me har blood group ka 1000ml stock rakh rahe hain
        self.blood_stock = {
            "A+": 1000, "A-": 1000, 
            "B+": 1000, "B-": 1000, 
            "O+": 1000, "O-": 1000, 
            "AB+": 1000, "AB-": 1000
        }
        self.blood_requests = []

    def process_request(self, req_id, hosp, req_bg, req_qty):
        available_qty = self.blood_stock.get(req_bg, 0)
        
        if available_qty < req_qty:
            raise BloodStockNotAvailableException(
                f"Sorry! Required qty {req_qty}ml unavailable for {req_bg}. Available: {available_qty}ml"
            )
        
        # Stock kam karenge
        self.blood_stock[req_bg] -= req_qty
        
        # Request save karenge tracking ke liye
        self.blood_requests.append({
            "req_id": req_id,
            "hospital": hosp,
            "blood_group": req_bg,
            "quantity": req_qty,
            "status": "Approved"
        })
        return True