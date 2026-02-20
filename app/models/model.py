from typing import Optional, Literal
from pydantic import BaseModel

class BusinessIncome(BaseModel):
    has_business_income: bool
    business_type: Optional[Literal[
        "freelancer", "consultant", "trader", "ecommerce", "retail", "service", "manufacturing", "other"
    ]] = None
    annual_gross_receipts: Optional[float] = 0.0
    annual_expenses: Optional[float] = 0.0
    under_presumptive_taxation: Optional[bool] = False

class IncomeDetails(BaseModel):
    basic_salary: float
    hra_received: float
    special_allowance: float
    bonus: float = 0.0
    other_income: float = 0.0  # Interest, rental, etc.
    business_income: Optional[BusinessIncome] = None

class RentDetails(BaseModel):
    monthly_rent_paid: float
    city_type: Literal["metro", "non-metro"]
    lives_in_rented_house: bool

class DeductionDetails(BaseModel):
    investments_under_80C: float = 0.0  # LIC, ELSS, PPF, tuition fees, etc.
    health_insurance_self_family: float = 0.0  # Health insurance (self + family)
    health_insurance_parents: float = 0.0  # Health insurance (parents)
    education_loan_interest: float = 0.0  # Education loan interest
    donations: float = 0.0  # Donations under 80G
    nps_additional_contribution: float = 0.0  # NPS under 80CCD(1B)
    home_loan_interest: float = 0.0  # Interest on housing loan (Section 24b)
    home_loan_principal: float = 0.0  # Principal repayment (falls under 80C)

class LoanDetails(BaseModel):
    has_home_loan: bool = False
    home_loan_interest: float = 0.0
    home_loan_principal: float = 0.0
    has_education_loan: bool = False
    education_loan_interest: float = 0.0

class basic(BaseModel):
    name: str
    age: int
    pan: Optional[str]
    employment_type: Literal["salaried", "self_employed", "freelancer", "pensioner"]
    resident_type: Literal["resident", "non_resident"]

class TaxSaverInput(BaseModel):
    basic: basic
    income: IncomeDetails
    rent: RentDetails
    deductions: DeductionDetails
    loans: LoanDetails

    preferred_tax_regime: Optional[Literal["old", "new"]] = None
