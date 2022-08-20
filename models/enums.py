from enum import Enum


class UserRole(Enum):
    Basic = "Basic"
    Premium = "Premium"
    admin = "Admin"


class AnalysisType(Enum):
    balance_sheet = "balance_sheet"
    recommendation = "recommendation"
    analysis = "analysis"
