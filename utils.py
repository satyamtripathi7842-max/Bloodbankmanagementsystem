import functools

# Custom Exceptions (Error Handling)
class InvalidDonorIDException(Exception): pass
class InvalidBloodGroupException(Exception): pass
class BloodStockNotAvailableException(Exception): pass
class ExpiredBloodUnitException(Exception): pass
class DuplicateDonorRegistrationException(Exception): pass

# Tuple used for fixed compatibility mappings
BLOOD_COMPATIBILITY = {
    "O-": ("O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"),
    "O+": ("O+", "A+", "B+", "AB+"),
    "A-": ("A-", "A+", "AB-", "AB+"),
    "A+": ("A+", "AB+"),
    "B-": ("B-", "B+", "AB-", "AB+"),
    "B+": ("B+", "AB+"),
    "AB-": ("AB-", "AB+"),
    "AB+": ("AB+",)
}

# Decorator for logging actions automatically
def log_action(action_name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print(f"\n✨ [LOG SYSTEM]: '{action_name}' successfully executed.")
            return result
        return wrapper
    return decorator

class BloodBankUtils:
    @staticmethod
    def is_compatible(donor_bg, recipient_bg):
        valid_groups = BLOOD_COMPATIBILITY.keys()
        if donor_bg not in valid_groups or recipient_bg not in valid_groups:
            raise InvalidBloodGroupException(f"Invalid group entry: {donor_bg} or {recipient_bg}")
        return recipient_bg in BLOOD_COMPATIBILITY[donor_bg]

    @classmethod
    def get_total_stock_capacity(cls, inventory_dict):
        return sum(inventory_dict.values())