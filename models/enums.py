from enum import Enum


class UserRole(Enum):
    Basic = "Basic"
    Premium = "Premium"
    admin = "Admin"


class ComplaintState(Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"
