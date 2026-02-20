def calculate_gross_income(data):
    income = data.income
    gross = income.basic_salary + income.hra_received + income.special_allowance + income.bonus + income.other_income
    if income.business_income and income.business_income.has_business_income:
        gross += income.business_income.annual_gross_receipts - income.business_income.annual_expenses
    return gross

def calculate_deductions(data):
    d = data.deductions
    total_80C = min(d.investments_under_80C + d.home_loan_principal, 150000)
    total_80D = min(d.health_insurance_self_family, 25000) + min(d.health_insurance_parents, 50000)
    total_80CCD = min(d.nps_additional_contribution, 50000)
    total = total_80C + total_80D + total_80CCD + d.education_loan_interest + d.donations + d.home_loan_interest
    return {
        "80C": total_80C,
        "80D": total_80D,
        "80CCD(1B)": total_80CCD,
        "education_loan_interest": d.education_loan_interest,
        "donations": d.donations,
        "home_loan_interest": d.home_loan_interest,
        "total_deductions": total
    }

def calculate_tax_old_regime(taxable_income, age):
    slabs = [
        (250000, 0.0),
        (500000, 0.05),
        (1000000, 0.2),
        (float("inf"), 0.3)
    ]
    return apply_slabs(taxable_income, slabs)

def calculate_tax_new_regime(gross_income, age):
    slabs = [
        (300000, 0.0),
        (600000, 0.05),
        (900000, 0.1),
        (1200000, 0.15),
        (1500000, 0.2),
        (float("inf"), 0.3)
    ]
    return apply_slabs(gross_income, slabs)

def apply_slabs(income, slabs):
    tax = 0
    previous_limit = 0
    for limit, rate in slabs:
        if income > limit:
            tax += (limit - previous_limit) * rate
            previous_limit = limit
        else:
            tax += (income - previous_limit) * rate
            break
    return round(tax)

def suggest_savings(data):
    s = {}
    if data.deductions.investments_under_80C + data.deductions.home_loan_principal < 150000:
        s["additional_80C_needed"] = 150000 - (data.deductions.investments_under_80C + data.deductions.home_loan_principal)
        s["suggested_instruments"] = ["PPF", "ELSS", "Life Insurance"]
    if data.deductions.health_insurance_self_family == 0:
        s["health_insurance_suggestion"] = "Consider purchasing health insurance to avail Section 80D deduction."
    return s

def calculate_exemptions(data):
    exemptions = {}
    if data.rent.lives_in_rented_house:
        hra = min(
            data.income.hra_received,
            0.5 * data.income.basic_salary if data.rent.city_type == "metro" else 0.4 * data.income.basic_salary,
            data.rent.monthly_rent_paid * 12 - 0.1 * data.income.basic_salary
        )
        exemptions["hra_exemption"] = max(hra, 0)
    exemptions["standard_deduction"] = 50000
    exemptions["home_loan_interest_deduction"] = min(data.deductions.home_loan_interest, 200000)
    return exemptions

def generate_alerts(data):
    alerts = []
    if data.deductions.investments_under_80C + data.deductions.home_loan_principal < 150000:
        alerts.append("You are under-utilizing your 80C limit.")
    if data.deductions.health_insurance_self_family == 0 and data.deductions.health_insurance_parents == 0:
        alerts.append("No health insurance claimed under 80D.")
    if data.deductions.donations > 0 and data.preferred_tax_regime == "new":
        alerts.append("Donations are not allowed under new regime.")
    return alerts

def generate_report_pdf(...):
    # Placeholder for now. Could use reportlab, weasyprint, or pdfkit.
    return "tax_report_vaibhav.pdf"
