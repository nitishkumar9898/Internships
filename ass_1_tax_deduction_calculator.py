     # TAX DEDUCTION CALCULATOR OLD VS NEW

def calculate_hra_exemption(basic_salary, hra_received, rent_paid, is_metro):
    
   city_limit = 0.5 if is_metro else 0.4
   excess_rent = max(0, rent_paid - 0.1 * basic_salary)
   return min(hra_received, excess_rent, city_limit * basic_salary)

def calculate_old_regime_tax(income, section_80c, basic_salary, hra_received, rent_paid, is_metro):
    
    standard_deduction = 50000
    hra_exemption = calculate_hra_exemption(basic_salary, hra_received, rent_paid, is_metro)
    section_80c = min(section_80c, 150000)  
    taxable_income = max(0, income - standard_deduction - section_80c - hra_exemption)

    
    if taxable_income <= 250000:
        tax = 0
    elif taxable_income <= 500000:
        tax = (taxable_income - 250000) * 0.05
    elif taxable_income <= 1000000:
        tax = 12500 + (taxable_income - 500000) * 0.20
    else:
        tax = 112500 + (taxable_income - 1000000) * 0.30

    
    cess = tax * 0.04
    return round(tax + cess), hra_exemption

def calculate_new_regime_tax(income):
    
    if income <= 300000:
        tax = 0
    elif income <= 600000:
        tax = (income - 300000) * 0.05
    elif income <= 900000:
        tax = 15000 + (income - 600000) * 0.10
    elif income <= 1200000:
        tax = 45000 + (income - 900000) * 0.15
    elif income <= 1500000:
        tax = 90000 + (income - 1200000) * 0.20
    else:
        tax = 150000 + (income - 1500000) * 0.30

  
    cess = tax * 0.04
    return round(tax + cess)

def get_valid_input(prompt, allow_zero=True):
    
    while True:
        try:
            value = float(input(prompt))
            if not allow_zero and value == 0:
                print("Value cannot be zero.")
                continue
            if value < 0:
                print("Please enter a non-negative value.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def display_results(ctc, bonus, section_80c, basic_salary, hra_received, rent_paid, is_metro, save_to_file=False):
  
    total_income = ctc + bonus
    old_tax, hra_exemption = calculate_old_regime_tax(
        total_income, section_80c, basic_salary, hra_received, rent_paid, is_metro
    )
    new_tax = calculate_new_regime_tax(total_income)

    
    output = [
        f"\n=== Tax Calculation Results ===",
        f"Total Income: Rs.{total_income:,.2f}",
        f"\nOld Regime Details:",
        f"  HRA Exemption: Rs.{hra_exemption:,.2f}",
        f"  80C Deduction: Rs.{section_80c:,.2f}",
        f"  Standard Deduction: Rs.50,000.00",
        f"  Tax Deduction: Rs.{old_tax:,.2f}",
        f"\nNew Regime Details:",
        f"  Tax Deduction: Rs.{new_tax:,.2f}",
    ]

   
    if old_tax < new_tax:
        savings = new_tax - old_tax
        output.append(f"You save Rs.{savings:,.2f} more using the Old Regime.")
    elif new_tax < old_tax:
        savings = old_tax - new_tax
        output.append(f"You save Rs.{savings:,.2f} more using the New Regime.")
    else:
        output.append("Both regimes result in the same tax amount.")

   
    for line in output:
        print(line)

    
    if save_to_file:
        with open("tax_calculation.txt", "w") as f:
            f.write("\n".join(output))
        print("\nResults saved to tax_calculation.txt")

def main():
    
    while True:
        print("\n=== Enhanced Tax Deduction Calculator ===")
        print("1. Calculate Tax")
        print("2. Exit")
        choice = input("Enter your choice (1-2): ")

        if choice == "1":
            # Get user inputs
            ctc = get_valid_input("Enter your CTC (in Rs.): ")
            bonus = get_valid_input("Enter your Bonus (in Rs.): ", allow_zero=True)
            section_80c = get_valid_input("Enter your 80C investment (in Rs., max 1,50,000): ", allow_zero=True)
            basic_salary = get_valid_input("Enter your Basic Salary (in Rs.): ")
            hra_received = get_valid_input("Enter your HRA received (in Rs.): ", allow_zero=True)
            rent_paid = get_valid_input("Enter your annual rent paid (in Rs.): ", allow_zero=True)
            is_metro = input("Do you live in a metro city? (y/n): ").lower() == "y"
            save_to_file = input("Save results to file? (y/n): ").lower() == "y"

            
            display_results(ctc, bonus, section_80c, basic_salary, hra_received, rent_paid, is_metro, save_to_file)
        elif choice == "2":
            print("Thank you for using the Tax Calculator. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()