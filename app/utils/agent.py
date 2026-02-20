from typing import Dict
import json
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Prompt template as a string (or load from file)
TAX_PROMPT = """
You are a Tax-Saving AI Assistant for Indian taxpayers.

Using the following user's financial information (formatted in JSON), generate a comprehensive tax-saving analysis report:

{user_data}

The report should include:

---

1. 📊 **Detailed Tax Calculation**
- Gross Total Income (sum of salary, business, rental, other income)
- Deductions under various sections (e.g. 80C, 80D, 80E, 24b, NPS)
- Net Taxable Income
- Tax payable under **Old** and **New** regimes
- Final recommendation: Which regime is better and by how much

2. 💰 **Savings Suggestions**
- How much more can be invested in **80C** to reach ₹1.5L
- Suggest investment options: PPF (low risk), ELSS (moderate risk)
- Suggest using **Section 80D**: Health insurance (self/family/parents) if not claimed

3. 🏠 **Exemption Suggestions**
- Calculate **HRA exemption** based on rent, city, and HRA received
- Ensure **Standard Deduction** (₹50,000) is applied
- Apply home loan deductions:
    - Interest (Section 24b)
    - Principal (Section 80C)

4. 🚨 **Optional Alerts**
- Any under-utilized deductions (80C, 80D, 80CCD)
- Missing insurance if user hasn’t claimed 80D
- Low tax-saving investments despite high income
- Overlapping or duplicate deduction claims

---

Use clear explanations, numeric examples, and short suggestions for improvements. Format your response professionally and concisely.
"""

def tax_saver_agent(user_data: Dict) -> str:
    """
    Takes user's structured financial input and returns a complete tax-saving report.
    """
    user_data_json = json.dumps(user_data, indent=2)
    prompt = PromptTemplate(
        input_variables=["user_data"],
        template=TAX_PROMPT
    ).format(user_data=user_data_json)

    llm = OpenAI(model="gpt-4", temperature=0.4, max_tokens=2500)
    response = llm(prompt)
    return response