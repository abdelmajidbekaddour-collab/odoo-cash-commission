# Cash-Based Sales Commission (Enterprise)

A professional solution for automating sales commissions in Odoo 18.0. This module calculates commissions based on **actual cash collection** (payment reconciliation), fully supporting partial payments, credit notes, and seamless integration with Odoo Payroll.

## 🚀 Key Features
- **Cash-Basis Calculation:** Commissions are generated only when the invoice is paid and reconciled.
- **Partial Payment Support:** Automatically handles partial reconciliations and calculates commission ratios accordingly.
- **Credit Note Integration:** Automatically deducts commissions if an invoice is returned or credited.
- **Multi-Employee Assignment:** Easily assign multiple beneficiaries to a single invoice or sale order.
- **Payroll Integration:** Pushes commission lines directly to the employee's payslip for seamless salary processing.
- **Smart Validation:** Built-in validation checks to prevent duplicate entries and data errors.

## ⚙️ Dependencies
This module requires the following standard Odoo modules:
- `sale`
- `account`
- `hr`
- `hr_payroll`
- `mail`

## 🛠 Installation
1. Ensure your Odoo instance is running (Version 18.0).
2. Copy the `cash_based_commission` folder into your Odoo `addons` path.
3. Restart your Odoo server.
4. Activate "Developer Mode" in Odoo.
5. Go to **Apps** -> **Update Apps List**.
6. Search for "Cash-Based Sales Commission" and click **Install**.

## ⚙️ Configuration & Usage

### 1. Payroll Configuration
To integrate the commission into the payroll system, follow these steps:
1. Go to **Payroll** -> **Configuration** -> **Salary Structures**.
2. Select the relevant **Salary Structure** (e.g., "Company Salary Structure").
3. Under the **Base for new structures** tab, click **Add a line**.
4. Select **Sales Commission (Cash)**. If it is not in the list, ensure the module is fully updated.

### 2. Computing Commissions
Once configured:
1. Create your commission periods via the **Commission Periods** menu.
2. Go to **Payroll** -> **Employee Payslips**.
3. Create a new payslip or open an existing one.
4. Click **Compute Sheet**.
5. The **Sales Commission (Cash)** line will automatically appear in the salary computation lines, based on the reconciled payments.

## 📧 Support & Customization
Need professional support or custom features? We provide tailored solutions for your business requirements.
- **Email:** [abdelmajidbekaddour@gmail.com]
- **Services:** Configuration, Customization, Support.

## 📄 License
This module is licensed under **OPL-1**. 
Copyright (c) 2026. All rights reserved.
