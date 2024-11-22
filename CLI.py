import numpy as np
import matplotlib.pyplot as plt

def get_user_input():
    """Get all necessary inputs from user via command line."""
    print("\n=== Savings Calculator ===\n")
    
    # Get basic inputs
    initial_savings = float(input("Initial Savings ($): "))
    monthly_spending = float(input("Monthly Spending ($): "))
    months = int(input("Projection Months: "))
    annual_interest_rate = float(input("Annual Interest Rate (%): ")) / 100
    
    # Get salary changes
    salary_schedule = []
    num_salary_changes = int(input("\nNumber of Salary Changes: "))
    
    for i in range(num_salary_changes):
        print(f"\nSalary Change {i+1}:")
        salary = float(input(f"Salary {i+1} ($/month): "))
        start_month = int(input("Starting Month: "))
        salary_schedule.append((salary, start_month))
    
    return initial_savings, monthly_spending, months, annual_interest_rate, salary_schedule

def calculate_savings(initial_savings, monthly_spending, months, annual_interest_rate, salary_schedule):
    """Calculate savings progression with multiple salary changes and compound interest."""
    monthly_interest_rate = annual_interest_rate / 12
    savings = np.zeros(months)
    savings[0] = initial_savings
    interest = np.zeros(months)
    interest[0] = 0
    
    # Sort salary changes by month
    salary_schedule.sort(key=lambda x: x[1])
    
    for i in range(1, months):
        # Find applicable salary for current month
        current_salary = 0
        for salary, start_month in salary_schedule:
            if i >= start_month - 1:  # -1 because months are 1-based in input
                current_salary = salary
        
        savings[i] = savings[i-1] * (1 + monthly_interest_rate) + current_salary - monthly_spending
        interest[i] = (savings[i-1] * monthly_interest_rate)
    
    return savings, interest

def plot_results(months, savings_projection, show_plot=True):
    """Create and display the savings projection plot."""
    plt.figure(figsize=(12, 6))
    plt.plot(range(months), savings_projection, marker='o', color='green')
    plt.title('Savings Projection')
    plt.xlabel('Months')
    plt.ylabel('Total Savings ($)')
    plt.grid(True)
    
    # Annotate final savings
    final_savings = savings_projection[-1]
    plt.annotate(
        f'Final Savings: ${final_savings:,.2f}',
        xy=(months-1, final_savings),
        xytext=(10, 10),
        textcoords='offset points'
    )
    
    plt.tight_layout()
    if show_plot:
        plt.show()

def print_results(savings_projection, interest_projection):
    """Print detailed breakdown of savings and interest."""
    print("\n=== Results ===\n")
    print("Monthly Savings Breakdown:")
    for month, amount in enumerate(savings_projection, 1):
        print(f"Month {month}: ${amount:,.2f}")
    
    total_interest = np.sum(interest_projection)
    print(f"\nTotal Interest Earned: ${total_interest:,.2f}")

def main():
    try:
        # Get user inputs
        initial_savings, monthly_spending, months, annual_interest_rate, salary_schedule = get_user_input()
        
        # Calculate savings
        savings_projection, interest_projection = calculate_savings(
            initial_savings,
            monthly_spending,
            months,
            annual_interest_rate,
            salary_schedule
        )
        
        # Display results
        print_results(savings_projection, interest_projection)
        plot_results(months, savings_projection)
        
    except ValueError as e:
        print("\nError: Please ensure all inputs are valid numbers.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()