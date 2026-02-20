// Handle conditional sections
document.getElementById('has_business_income').addEventListener('change', function() {
    document.getElementById('business_details').classList.toggle('hidden', !this.checked);
});

document.getElementById('has_home_loan').addEventListener('change', function() {
    document.getElementById('home_loan_details').classList.toggle('hidden', !this.checked);
});

document.getElementById('has_education_loan').addEventListener('change', function() {
    document.getElementById('education_loan_details').classList.toggle('hidden', !this.checked);
});

function generateJSON() {
    const formData = {
        basic: {
            name: document.getElementById('name').value,
            age: parseInt(document.getElementById('age').value) || 0,
            pan: document.getElementById('pan').value || null,
            employment_type: document.getElementById('employment_type').value,
            resident_type: document.getElementById('resident_type').value
        },
        income: {
            basic_salary: parseFloat(document.getElementById('basic_salary').value) || 0,
            hra_received: parseFloat(document.getElementById('hra_received').value) || 0,
            special_allowance: parseFloat(document.getElementById('special_allowance').value) || 0,
            bonus: parseFloat(document.getElementById('bonus').value) || 0,
            other_income: parseFloat(document.getElementById('other_income').value) || 0,
            business_income: document.getElementById('has_business_income').checked ? {
                has_business_income: true,
                business_type: document.getElementById('business_type').value || null,
                annual_gross_receipts: parseFloat(document.getElementById('annual_gross_receipts').value) || 0,
                annual_expenses: parseFloat(document.getElementById('annual_expenses').value) || 0,
                under_presumptive_taxation: document.getElementById('under_presumptive_taxation').checked
            } : {
                has_business_income: false,
                business_type: null,
                annual_gross_receipts: 0,
                annual_expenses: 0,
                under_presumptive_taxation: false
            }
        },
        rent: {
            monthly_rent_paid: parseFloat(document.getElementById('monthly_rent_paid').value) || 0,
            city_type: document.getElementById('city_type').value,
            lives_in_rented_house: document.getElementById('lives_in_rented_house').checked
        },
        deductions: {
            investments_under_80C: parseFloat(document.getElementById('investments_under_80C').value) || 0,
            health_insurance_self_family: parseFloat(document.getElementById('health_insurance_self_family').value) || 0,
            health_insurance_parents: parseFloat(document.getElementById('health_insurance_parents').value) || 0,
            education_loan_interest: parseFloat(document.getElementById('education_loan_interest').value) || 0,
            donations: parseFloat(document.getElementById('donations').value) || 0,
            nps_additional_contribution: parseFloat(document.getElementById('nps_additional_contribution').value) || 0,
            home_loan_interest: parseFloat(document.getElementById('home_loan_interest_deduction').value) || 0,
            home_loan_principal: parseFloat(document.getElementById('home_loan_principal_deduction').value) || 0
        },
        loans: {
            has_home_loan: document.getElementById('has_home_loan').checked,
            home_loan_interest: parseFloat(document.getElementById('home_loan_interest').value) || 0,
            home_loan_principal: parseFloat(document.getElementById('home_loan_principal').value) || 0,
            has_education_loan: document.getElementById('has_education_loan').checked,
            education_loan_interest: parseFloat(document.getElementById('education_loan_interest_loan').value) || 0
        },
        preferred_tax_regime: document.getElementById('preferred_tax_regime').value || null
    };

    document.getElementById('json-output').value = JSON.stringify(formData, null, 2);
    document.getElementById('output').classList.remove('hidden');
    document.getElementById('output').scrollIntoView({ behavior: 'smooth' });
}

function copyToClipboard() {
    const textarea = document.getElementById('json-output');
    textarea.select();
    document.execCommand('copy');
    alert('JSON copied to clipboard!');
}

async function sendToApi() {
    const json = document.getElementById('json-output').value;
    if (!json.trim()) {
        alert('Please generate JSON first!');
        return;
    }
    document.getElementById('tax-report-section').classList.remove('hidden');
    document.getElementById('tax-report').innerText = "Loading...";
    try {
        const res = await fetch('/tax-saver-agent/generate-report', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: json
        });
        const data = await res.json();
        document.getElementById('tax-report').innerText = data.report || "No report received.";
    } catch (err) {
        document.getElementById('tax-report').innerText = "Error: " + err;
    }
}

// Form validation
document.querySelector('.submit-btn').addEventListener('click', function(e) {
    const requiredFields = document.querySelectorAll('input[required], select[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#e74c3c';
            isValid = false;
        } else {
            field.style.borderColor = '#e1e5e9';
        }
    });
    
    if (!isValid) {
        alert('Please fill all required fields!');
        return;
    }
});