import matplotlib.pyplot as plt
def npv(rate, cash_flows):
    #Computes NPV.
    #Formula: Sum( C_t / (1+r)^t )
    total = 0
    for t, cash in enumerate(cash_flows):
        total += cash / ((1 + rate) ** t)
    return total

def irr(cash_flows):
   # Robust Bisection Method for IRR.
   # Handles both Investing (NPV goes down) and Financing (NPV goes up).
    # Search Range: -99% to 1000%
    low = -0.99
    high = 10.0
    tolerance = 1e-6
    
    # Check boundary signs
    npv_low = npv(low, cash_flows)
    npv_high = npv(high, cash_flows)
    
    # If both are positive or both negative, there is no simple IRR in this range
    if npv_low * npv_high > 0:
        return None

    for i in range(1000):
        mid = (low + high) / 2
        npv_mid = npv(mid, cash_flows)
        
        # Found the root?
        if abs(npv_mid) < tolerance:
            return mid
        
        # Determine which side the root is on
        # If npv_low and npv_mid have the SAME sign, the root is NOT between them.
        # It must be in the upper half.
        if npv_low * npv_mid > 0:
            low = mid
            npv_low = npv_mid 
        else:
            high = mid
            
    return (low + high) / 2


def analyze_project(name, cash_flows):
    print(f"\n{'-'*10} {name} {'-'*10}")
    print(f"Cash Flows: {cash_flows}")
    
    # Calculate IRR
    project_irr = irr(cash_flows)
    if project_irr:
        print(f"IRR: {project_irr:.2%}")
    else:
        print("IRR: No valid solution in range")
        
    # Sensitivity Table
    rates = [0.0, 0.05, 0.10, 0.15, 0.20]
    print("\nNPV Sensitivity:")
    for r in rates:
        print(f"  @{r:>4.0%}: ₹{npv(r, cash_flows):,.2f}")

    # Plotting 
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    plt.subplots_adjust(hspace=0.4)

    # Plot 1: Cash Flow Diagram (Bar Chart)
    colors = ['green' if c >= 0 else 'red' for c in cash_flows]
    periods = range(len(cash_flows))
    ax1.bar(periods, cash_flows, color=colors, alpha=0.7)
    ax1.axhline(0, color='black', linewidth=1)
    ax1.set_title(f"Cash Flow Diagram: {name}")
    ax1.set_ylabel("Amount (₹)")
    ax1.set_xlabel("Time Period (Year)")
    ax1.set_xticks(periods)
    
    # Add labels on bars
    for t, v in enumerate(cash_flows):
        ax1.text(t, v, f"{v}", ha='center', va='bottom' if v>0 else 'top', fontsize=9)

    # Plot 2: NPV Profile
    plot_rates = [i/100 for i in range(0, 41)] # 0% to 40%
    plot_npvs = [npv(r, cash_flows) for r in plot_rates]
    
    ax2.plot([r*100 for r in plot_rates], plot_npvs, label="NPV Profile", color='blue')
    ax2.axhline(0, color='black', linestyle='--')
    
    if project_irr:
        # Mark the IRR
        irr_pct = project_irr * 100
        ax2.plot(irr_pct, 0, 'ro', markersize=8, label=f"IRR: {project_irr:.2%}")
        ax2.annotate(f"{project_irr:.2%}", (irr_pct, 0), xytext=(irr_pct, max(plot_npvs)/5),
                     arrowprops=dict(facecolor='black', shrink=0.05))

    ax2.set_title("NPV Profile (Value vs Discount Rate)")
    ax2.set_xlabel("Discount Rate (%)")
    ax2.set_ylabel("Net Present Value (₹)")
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.show()


# Test A: Uneven Cash Flows (Investment)
# Initial Outflow (-), followed by positive inflows
analyze_project("Uneven Investment", [-10000, 3000, 4000, 5000])

# Test B: Financing Project (Loan) 
# Initial Inflow (+) (Loan received), followed by negative outflows (Repayment)
# Note: NPV curve for this will go UP as rate increases.
analyze_project("Financing (Loan)", [10000, -3000, -3000, -3000, -3000])

# Test C: Annuity
analyze_project("Annuity", [-50000, 15000, 15000, 15000, 15000])