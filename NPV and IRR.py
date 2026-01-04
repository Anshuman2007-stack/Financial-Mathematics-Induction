import matplotlib.pyplot as plt
import numpy as np

def get_npv(rate, cash_flows):
    if rate <= -1: return float('inf')
    npv = 0
    for t, val in enumerate(cash_flows):
        npv += val / ((1 + rate) ** t)
    return npv

def get_irrs(cash_flows):
    found_irrs = []
    # Scanning from -99% to 1000%
    r = -0.99
    limit = 10.0
    step = 0.01
    
    while r < limit:
        r_next = r + step
        val1 = get_npv(r, cash_flows)
        val2 = get_npv(r_next, cash_flows)
        if val1 * val2 < 0:
         low = r
         high = r_next
         for _ in range(100):
            mid = (low + high) / 2
            mid_val = get_npv(mid, cash_flows)
            if abs(mid_val) < 1e-6:
                found_irrs.append(mid)
                break
            if get_npv(low, cash_flows) * mid_val < 0:
                high = mid
            else:
                low = mid
         else:
            found_irrs.append((low + high) / 2)
        elif val1*val2==0:
            if val1==0:
                found_irrs.append(r)         
        r += step
    return found_irrs

scenarios = [
    {"name": "Uneven Cashflows", "flows": [-10000, 3000, 4000, 5000]},
    {"name": "Loan/Financing",   "flows": [10000, -3000, -3000, -3000, -3000]},
    {"name": "Annuity",     "flows": [-50000, 15000, 15000, 15000, 15000]},
    {"name": "Multiple IRR's", "flows":[-100, 230, -132]}
]

for i, scenario in enumerate(scenarios):
    name = scenario["name"]
    flows = scenario["flows"]
    
    print(f"\n{'='*40}")
    print(f"ANALYZING: {name}")
    print(f"Cash Flows: {flows}")
    
    # Calculate IRR
    results = get_irrs(flows)
    
    # Print Results
    if not results:
        print(">> Result: No IRR found")
    else:
        for idx, rate in enumerate(results):
            print(f">> IRR {idx+1}: {rate*100:.2f}%")

    # Plotting
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Graph 1: Cash Flow Bars
    colors = ['green' if x >= 0 else 'red' for x in flows]
    ax1.bar(range(len(flows)), flows, color=colors, alpha=0.7)
    ax1.axhline(0, color='black', linewidth=1)
    ax1.set_title(f'{name}\nCash Flow Diagram')
    ax1.set_ylabel('Amount')
    ax1.set_xlabel('Year')
    
    # Graph 2: NPV Curve
    x = np.linspace(-0.5, 0.5, 200)
    y = [get_npv(r, flows) for r in x]
    
    ax2.plot(x*100, y, label='NPV Curve', color='blue')
    ax2.axhline(0, color='black', linestyle='--')
    
    for rate in results:
        ax2.scatter(rate*100, 0, color='red', s=100, label=f'IRR: {rate*100:.2f}%', zorder=5)
    
    ax2.set_title(f'NPV Profile')
    ax2.set_xlabel('Discount Rate (%)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.show()
    
