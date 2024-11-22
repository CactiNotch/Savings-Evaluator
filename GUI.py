import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import sys
matplotlib.use('TkAgg')

class SavingsCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Savings Calculator")

        if sys.platform.startswith('win'):
            self.root.state('zoomed')
        else:
            self.root.state('-zoomed', True)

        # Create main frames
        self.input_frame = ttk.Frame(root, padding="10")
        self.input_frame.grid(row=0, column=0, sticky="nsew")
        
        self.plot_frame = ttk.Frame(root, padding="10")
        self.plot_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")
        
        self.results_frame = ttk.Frame(root, padding="10")
        self.results_frame.grid(row=1, column=0, sticky="nsew")
        
        # Configure grid weights
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)
        
        # Store salary change entries
        self.salary_changes = []  
        
        self.create_input_widgets()
        self.create_plot()
        self.create_results_widgets()
        
    def create_input_widgets(self):
        # Input fields
        labels = [
            "Initial Savings ($):",
            "Monthly Spending ($):",
            "Projection Months:",
            "Annual Interest Rate (%):"
        ]
        
        default_values = [1000, 500, 12, 5]
        self.inputs = {}
        
        for i, (label, default) in enumerate(zip(labels, default_values)):
            ttk.Label(self.input_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            var = tk.StringVar(value=str(default))
            entry = ttk.Entry(self.input_frame, textvariable=var)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.inputs[label] = var

        # Salary changes section
        ttk.Label(self.input_frame, text="Number of Salary Changes:").grid(
            row=len(labels), column=0, padx=5, pady=5, sticky="e"
        )
        self.salary_changes_var = tk.StringVar(value="1")
        salary_spinner = ttk.Spinbox(
            self.input_frame,
            from_=1,
            to=10,
            textvariable=self.salary_changes_var,
            width=5,
            command=self.update_salary_entries
        )
        salary_spinner.grid(row=len(labels), column=1, padx=5, pady=5, sticky="w")
        
        # Frame for salary change entries
        self.salary_frame = ttk.Frame(self.input_frame)
        self.salary_frame.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)
        
        # Initial salary entries
        self.update_salary_entries()
        
        # Calculate button (moved to bottom)
        ttk.Button(self.input_frame, text="Calculate", command=self.update_calculation).grid(
            row=len(labels)+2, column=0, columnspan=2, pady=20
        )
        
    def update_salary_entries(self):
        # Store current values before clearing widgets
        current_values = []
        for salary_var, month_var in self.salary_changes:
            current_values.append((salary_var.get(), month_var.get()))
        
        # Clear existing salary entries
        for widget in self.salary_frame.winfo_children():
            widget.destroy()
        self.salary_changes.clear()
        
        num_changes = int(self.salary_changes_var.get())
        
        # Create new salary entries
        for i in range(num_changes):
            frame = ttk.Frame(self.salary_frame)
            frame.grid(row=i, column=0, pady=5)
            
            # Salary amount
            ttk.Label(frame, text=f"Salary {i+1} ($/month):").grid(row=0, column=0, padx=5)
            salary_value = current_values[i][0] if i < len(current_values) else "2000"
            salary_var = tk.StringVar(value=salary_value)
            salary_entry = ttk.Entry(frame, textvariable=salary_var, width=10)
            salary_entry.grid(row=0, column=1, padx=5)
            
            # Month of change
            ttk.Label(frame, text="Starting Month:").grid(row=0, column=2, padx=5)
            month_value = current_values[i][1] if i < len(current_values) else str(i * 3 + 1)
            month_var = tk.StringVar(value=month_value)
            month_entry = ttk.Entry(frame, textvariable=month_var, width=5)
            month_entry.grid(row=0, column=3, padx=5)
            
            self.salary_changes.append((salary_var, month_var))
        
    def create_plot(self):
        self.fig = Figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_results_widgets(self):
        self.result_text = tk.Text(self.results_frame, height=10, width=40)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
    def calculate_savings(self, initial_savings, monthly_spending, months, annual_interest_rate):
        monthly_interest_rate = annual_interest_rate / 12
        savings = np.zeros(months)
        savings[0] = initial_savings
        interest = np.zeros(months)
        interest[0] = 0
        
        # Sort salary changes by month
        salary_schedule = [(float(salary.get()), int(month.get())) 
                          for salary, month in self.salary_changes]
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
        
    def update_calculation(self):
        try:
            # Get input values
            initial_savings = float(self.inputs["Initial Savings ($):"].get())
            monthly_spending = float(self.inputs["Monthly Spending ($):"].get())
            months = int(self.inputs["Projection Months:"].get())
            annual_interest_rate = float(self.inputs["Annual Interest Rate (%):"].get()) / 100
            
            # Calculate
            savings_projection, interest_projection = self.calculate_savings(
                initial_savings, monthly_spending, months, annual_interest_rate
            )
            
            # Update plot
            self.ax.clear()
            self.ax.plot(range(months), savings_projection, marker='o', color='green')
            self.ax.set_title('Savings Projection')
            self.ax.set_xlabel('Months')
            self.ax.set_ylabel('Total Savings ($)')
            self.ax.grid(True)
            
            # Annotate final savings
            final_savings = savings_projection[-1]
            self.ax.annotate(
                f'Final Savings: ${final_savings:,.2f}',
                xy=(months-1, final_savings),
                xytext=(-50, 10),
                textcoords='offset points'
            )
            
            self.canvas.draw()
            
            # Update results text
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Monthly Savings Breakdown:\n\n")
            for month, amount in enumerate(savings_projection, 1):
                self.result_text.insert(tk.END, f"Month {month}: ${amount:,.2f}\n")
            
            total_interest = np.sum(interest_projection)
            self.result_text.insert(tk.END, f"\nTotal Interest Earned: ${total_interest:,.2f}")
            
        except ValueError as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Error: Please check that all inputs are valid numbers.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SavingsCalculatorGUI(root)
    root.mainloop()