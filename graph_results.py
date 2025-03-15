import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D

# Create directories if they don't exist
os.makedirs('graphs', exist_ok=True)
os.makedirs('graphs/grid_layouts', exist_ok=True)

# Set a more aesthetically pleasing style
plt.style.use('seaborn-v0_8-whitegrid')

# Define better colors for domains and approaches
domain_colors = {
    'termes': '#1f77b4',      # blue
    'blocksworld': '#ff7f0e', # orange
    'tyreworld': '#2ca02c',   # green
    'grippers': '#d62728',    # red
    'barman': '#9467bd'       # purple
}

approach_colors = {
    'multiagent': '#2471A3',  # darker blue
    'twostep': '#E74C3C'      # red
}

markers = ['o', 's', '^', 'D', 'v']
domains = ['termes', 'blocksworld', 'tyreworld', 'grippers', 'barman']

# Original multiagent results
results_dict = {
    # Single agent results (n=1)
    'termes-1': {'avg_planning_time': 813.42, 'avg_solution_cost': 92.10, 'timeouts': 0},
    'termes-2': {'avg_planning_time': 966.27, 'avg_solution_cost': 138.20, 'timeouts': 0},
    'termes-3': {'avg_planning_time': 1000.34, 'avg_solution_cost': 153.71, 'timeouts': 3},
    'termes-4': {'avg_planning_time': 1000.47, 'avg_solution_cost': 194.07, 'timeouts': 5},
    'termes-5': {'avg_planning_time': 1000.55, 'avg_solution_cost': 164.00, 'timeouts': 16},
    
    'blocksworld-1': {'avg_planning_time': 268.97, 'avg_solution_cost': 17.70, 'timeouts': 0},
    'blocksworld-2': {'avg_planning_time': 293.18, 'avg_solution_cost': 15.55, 'timeouts': 0},
    'blocksworld-3': {'avg_planning_time': 316.77, 'avg_solution_cost': 14.35, 'timeouts': 0},
    'blocksworld-4': {'avg_planning_time': 375.80, 'avg_solution_cost': 13.80, 'timeouts': 0},
    'blocksworld-5': {'avg_planning_time': 383.52, 'avg_solution_cost': 13.55, 'timeouts': 0},
    
    'tyreworld-1': {'avg_planning_time': 953.35, 'avg_solution_cost': 121.35, 'timeouts': 0},
    'tyreworld-2': {'avg_planning_time': 603.58, 'avg_solution_cost': 121.35, 'timeouts': 0},
    'tyreworld-3': {'avg_planning_time': 563.37, 'avg_solution_cost': 121.35, 'timeouts': 0},
    'tyreworld-4': {'avg_planning_time': 407.79, 'avg_solution_cost': 121.35, 'timeouts': 0},
    'tyreworld-5': {'avg_planning_time': 412.96, 'avg_solution_cost': 121.35, 'timeouts': 0},
    
    'grippers-1': {'avg_planning_time': 1.18, 'avg_solution_cost': 8.60, 'timeouts': 0},
    'grippers-2': {'avg_planning_time': 85.56, 'avg_solution_cost': 8.50, 'timeouts': 0},
    'grippers-3': {'avg_planning_time': 88.15, 'avg_solution_cost': 7.45, 'timeouts': 0},
    'grippers-4': {'avg_planning_time': 61.08, 'avg_solution_cost': 7.35, 'timeouts': 0},
    'grippers-5': {'avg_planning_time': 73.88, 'avg_solution_cost': 7.35, 'timeouts': 0},
    
    'barman-1': {'avg_planning_time': 1001.41, 'avg_solution_cost': 56.20, 'timeouts': 0},
    'barman-2': {'avg_planning_time': 1000.36, 'avg_solution_cost': 49.15, 'timeouts': 0},
    'barman-3': {'avg_planning_time': 1000.35, 'avg_solution_cost': 49.15, 'timeouts': 0},
    'barman-4': {'avg_planning_time': 1000.44, 'avg_solution_cost': 50.55, 'timeouts': 0},
    'barman-5': {'avg_planning_time': 1000.55, 'avg_solution_cost': 50.50, 'timeouts': 0}
}

# Two-step approach data with multiple runs
twostep_data = {
    'barman': {
        2: {'runs': [(717.10, 51.00), (732.30, 51.45), (744.21, 51.45)]},
        3: {'runs': [(667.67, 49.05), (644.99, 49.30), (644.10, 49.35)]},
        4: {'runs': [(568.66, 49.05), (573.92, 49.15), (571.89, 49.15)]},
        5: {'runs': [(631.85, 49.65), (502.12, 46.83), (547.94, 49.40)]}
    },
    'blocksworld': {
        2: {'runs': [(138.39, 18.25), (160.70, 18.75), (160.47, 18.75)]},
        3: {'runs': [(117.10, 19.65), (107.41, 19.40), (107.29, 19.95)]},
        4: {'runs': [(75.33, 19.70), (74.69, 19.90), (86.87, 20.10)]},
        5: {'runs': [(70.08, 21.60), (80.28, 21.70), (85.63, 20.45)]}
    },
    'grippers': {
        2: {'runs': [(1.85, 7.75), (2.21, 6.95), (2.24, 6.80)]},
        3: {'runs': [(2.42, 6.10), (3.03, 5.85), (2.71, 5.75)]},
        4: {'runs': [(2.88, 5.25), (3.38, 5.10), (3.29, 5.35)]},
        5: {'runs': [(3.23, 5.95), (4.01, 5.05), (2.42, 5.85)]}
    },
    'termes': {
        2: {'runs': [(513.31, 99.70), (508.23, 98.60), (483.86, 94.30)]},
        3: {'runs': [(402.16, 117.30), (423.61, 116.95), (349.08, 109.85)]},
        4: {'runs': [(276.06, 107.75), (278.29, 104.95), (318.53, 110.75)]},
        5: {'runs': [(291.38, 113.90), (243.18, 120.38), (234.79, 110.81)]}
    },
    'tyreworld': {
        2: {'runs': [(482.60, 113.50), (483.91, 112.20), (483.39, 112.15)]},
        3: {'runs': [(354.27, 108.15), (360.68, 108.45), (409.58, 108.30)]},
        4: {'runs': [(322.95, 112.40), (353.46, 106.05), (315.78, 109.05)]},
        5: {'runs': [(257.83, 112.30), (209.56, 113.85), (209.32, 114.35)]}
    }
}

# Calculate statistics for two-step approach
for domain in twostep_data:
    for n in twostep_data[domain]:
        runs = twostep_data[domain][n]['runs']
        planning_times = [run[0] for run in runs]
        solution_costs = [run[1] for run in runs]
        
        twostep_data[domain][n]['avg_planning_time'] = np.mean(planning_times)
        twostep_data[domain][n]['avg_solution_cost'] = np.mean(solution_costs)
        twostep_data[domain][n]['std_planning_time'] = np.std(planning_times)
        twostep_data[domain][n]['std_solution_cost'] = np.std(solution_costs)

# Function to create individual domain plots
def create_domain_plot(domain, metric, ylabel, title_suffix):
    plt.figure(figsize=(10, 6))
    
    # Multiagent approach data
    x_values = []
    y_values = []
    
    for n in range(1, 5):  # Changed to only go up to 4 agents
        key = f'{domain}-{n}'
        if key in results_dict:
            x_values.append(n)
            y_values.append(results_dict[key][metric])
    
    plt.plot(x_values, y_values, 
            label="Multiagent Approach",
            color=approach_colors['multiagent'],
            marker='o',
            linewidth=3,
            markersize=10,
            linestyle='-')
    
    # Two-step approach data
    if domain in twostep_data:
        x_values_twostep = [n for n in sorted(twostep_data[domain].keys()) if n <= 4]  # Only include up to 4 agents
        y_values_twostep = [twostep_data[domain][n][metric] for n in x_values_twostep]
        y_std_twostep = [twostep_data[domain][n][f'std_{metric.replace("avg_", "")}'] for n in x_values_twostep]
        
        plt.plot(x_values_twostep, y_values_twostep,
                label="Two-step Approach",
                color=approach_colors['twostep'],
                marker='s',
                linewidth=3,
                markersize=10,
                linestyle='--')
        
        plt.fill_between(x_values_twostep, 
                        [max(0, y - std) for y, std in zip(y_values_twostep, y_std_twostep)],
                        [y + std for y, std in zip(y_values_twostep, y_std_twostep)],
                        color=approach_colors['twostep'], alpha=0.2)
    
    plt.xlabel('Number of Agents', fontsize=14, fontweight='bold')
    plt.ylabel(ylabel, fontsize=14, fontweight='bold')
    plt.title(f'{domain.capitalize()} Domain {title_suffix}', fontsize=16, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12, frameon=True, fancybox=True, shadow=True)
    plt.xticks(range(1, 5), fontsize=12)  # Changed to only show up to 4 agents
    plt.yticks(fontsize=12)
    
    # Add a light background color
    ax = plt.gca()
    ax.set_facecolor('#f8f9fa')
    
    # Add a border
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(1)
    
    # Save individual plot
    plt.tight_layout()
    plt.savefig(f'graphs/{domain}_{metric}_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

# Function to create grid layout with properly normalized standard deviation
def create_combined_grid_layout():
    plt.figure(figsize=(18, 7))
    gs = GridSpec(2, 6, figure=plt.gcf(), hspace=0.2, wspace=0.35)
    
    # Create a single legend for the entire figure
    legend_elements = [
        Line2D([0], [0], color=approach_colors['multiagent'], marker='o', linestyle='-', 
               linewidth=2, markersize=8, label='MA PDDL'),
        Line2D([0], [0], color=approach_colors['twostep'], marker='s', linestyle='--', 
               linewidth=2, markersize=8, label='TWOSTEP')
    ]
    
    # Store normalized data for averaging
    normalized_planning_time = {
        'multiagent': {n: [] for n in range(1, 5)},
        'twostep': {n: [] for n in range(2, 5)}
    }
    
    normalized_solution_cost = {
        'multiagent': {n: [] for n in range(1, 5)},
        'twostep': {n: [] for n in range(2, 5)}
    }
    
    # Store normalized standard deviations for two-step approach
    normalized_planning_time_std = {n: [] for n in range(2, 5)}
    normalized_solution_cost_std = {n: [] for n in range(2, 5)}
    
    for idx, domain in enumerate(domains):
        # Top row - Planning Time
        ax_time = plt.subplot(gs[0, idx])
        ax_time.set_facecolor('#f8f9fa')  # Add light gray background
        
        # Multiagent approach data - planning time
        x_values = []
        y_values = []
        
        for n in range(1, 5):  # Changed to only go up to 4 agents
            key = f'{domain}-{n}'
            if key in results_dict:
                x_values.append(n)
                y_values.append(results_dict[key]['avg_planning_time'])
        
        # Normalize planning time for multiagent approach
        if y_values:
            max_time = max(y_values)
            for n, time in zip(range(1, 5), y_values):  # Changed to only go up to 4 agents
                normalized_planning_time['multiagent'][n].append(time / max_time if max_time > 0 else 0)
        
        ax_time.plot(x_values, y_values, 
               color=approach_colors['multiagent'],
               marker='o',
               linewidth=2,
               markersize=6,
               linestyle='-')
        
        # Two-step approach data - planning time
        if domain in twostep_data:
            x_values_twostep = [n for n in sorted(twostep_data[domain].keys()) if n <= 4]  # Only include up to 4 agents
            y_values_twostep = [twostep_data[domain][n]['avg_planning_time'] for n in x_values_twostep]
            y_std_twostep = [twostep_data[domain][n]['std_planning_time'] for n in x_values_twostep]
            
            # Normalize planning time and std for two-step approach
            if y_values and y_values_twostep:
                max_time = max(max(y_values), max(y_values_twostep))
                for n, time, std in zip(x_values_twostep, y_values_twostep, y_std_twostep):
                    norm_factor = max_time if max_time > 0 else 1
                    normalized_planning_time['twostep'][n].append(time / norm_factor)
                    # Normalize std by the same factor
                    normalized_planning_time_std[n].append(std / norm_factor)
            
            ax_time.plot(x_values_twostep, y_values_twostep,
                   color=approach_colors['twostep'],
                   marker='s',
                   linewidth=2,
                   markersize=6,
                   linestyle='--')
            
            ax_time.fill_between(x_values_twostep, 
                           [max(0, y - std) for y, std in zip(y_values_twostep, y_std_twostep)],
                           [y + std for y, std in zip(y_values_twostep, y_std_twostep)],
                           color=approach_colors['twostep'], alpha=0.2)
        
        # Only add y-label to the first plot in each row
        if idx == 0:
            ax_time.set_ylabel('Planning Time (s)', fontsize=12, fontweight='bold')
        
        ax_time.set_title(f'{domain.capitalize()}', fontsize=12, fontweight='bold')
        ax_time.grid(True, linestyle='--', alpha=0.7)
        ax_time.set_xticks(range(1, 5))  # Changed to only show up to 4 agents
        ax_time.tick_params(axis='both', labelsize=10)  # Slightly smaller tick labels
        
        # Bottom row - Execution Length (formerly Solution Cost)
        ax_cost = plt.subplot(gs[1, idx])
        ax_cost.set_facecolor('#f8f9fa')  # Add light gray background
        
        # Multiagent approach data - execution length
        x_values = []
        y_values = []
        
        for n in range(1, 5):  # Changed to only go up to 4 agents
            key = f'{domain}-{n}'
            if key in results_dict:
                x_values.append(n)
                y_values.append(results_dict[key]['avg_solution_cost'])
        
        # Normalize execution length for multiagent approach
        if y_values:
            max_cost = max(y_values)
            for n, cost in zip(range(1, 5), y_values):  # Changed to only go up to 4 agents
                normalized_solution_cost['multiagent'][n].append(cost / max_cost if max_cost > 0 else 0)
        
        ax_cost.plot(x_values, y_values, 
               color=approach_colors['multiagent'],
               marker='o',
               linewidth=2,
               markersize=6,
               linestyle='-')
        
        # Two-step approach data - execution length
        if domain in twostep_data:
            x_values_twostep = [n for n in sorted(twostep_data[domain].keys()) if n <= 4]  # Only include up to 4 agents
            y_values_twostep = [twostep_data[domain][n]['avg_solution_cost'] for n in x_values_twostep]
            y_std_twostep = [twostep_data[domain][n]['std_solution_cost'] for n in x_values_twostep]
            
            # Normalize execution length and std for two-step approach
            if y_values and y_values_twostep:
                max_cost = max(max(y_values), max(y_values_twostep))
                for n, cost, std in zip(x_values_twostep, y_values_twostep, y_std_twostep):
                    norm_factor = max_cost if max_cost > 0 else 1
                    normalized_solution_cost['twostep'][n].append(cost / norm_factor)
                    # Normalize std by the same factor
                    normalized_solution_cost_std[n].append(std / norm_factor)
            
            ax_cost.plot(x_values_twostep, y_values_twostep,
                   color=approach_colors['twostep'],
                   marker='s',
                   linewidth=2,
                   markersize=6,
                   linestyle='--')
            
            ax_cost.fill_between(x_values_twostep, 
                           [max(0, y - std) for y, std in zip(y_values_twostep, y_std_twostep)],
                           [y + std for y, std in zip(y_values_twostep, y_std_twostep)],
                           color=approach_colors['twostep'], alpha=0.2)
        
        # Only add y-label to the first plot in each row
        if idx == 0:
            ax_cost.set_ylabel('Execution Length', fontsize=12, fontweight='bold')
        
        ax_cost.set_xlabel('Number of Agents', fontsize=10, fontweight='bold')
        ax_cost.grid(True, linestyle='--', alpha=0.7)
        ax_cost.set_xticks(range(1, 5))  # Changed to only show up to 4 agents
        ax_cost.tick_params(axis='both', labelsize=10)  # Slightly smaller tick labels
    
    # Add average planning time plot (top right)
    ax_avg_time = plt.subplot(gs[0, 5])
    ax_avg_time.set_facecolor('#f8f9fa')  # Add light gray background
    
    # Calculate average normalized planning time for multiagent approach
    x_values_multi = list(range(1, 5))  # Changed to only go up to 4 agents
    y_values_multi = [np.mean(normalized_planning_time['multiagent'][n]) for n in x_values_multi]
    
    # Calculate average normalized planning time and std for two-step approach
    x_values_twostep = list(range(2, 5))  # Changed to only go up to 4 agents
    y_values_twostep = [np.mean(normalized_planning_time['twostep'][n]) for n in x_values_twostep]
    # Average the normalized standard deviations
    y_std_twostep = [np.mean(normalized_planning_time_std[n]) for n in x_values_twostep]
    
    # Print statistics for normalized planning time
    print("\n=== Normalized Planning Time Statistics ===")
    print("Multiagent approach:")
    for n, value in zip(x_values_multi, y_values_multi):
        print(f"  {n} agents: {value:.4f}")
    
    print("\nTwo-step approach:")
    for n, value, std in zip(x_values_twostep, y_values_twostep, y_std_twostep):
        print(f"  {n} agents: {value:.4f} ± {std:.4f}")
    
    # Plot average planning time
    ax_avg_time.plot(x_values_multi, y_values_multi,
                    color=approach_colors['multiagent'],
                    marker='o',
                    linewidth=3,
                    markersize=8,
                    linestyle='-')
    
    ax_avg_time.plot(x_values_twostep, y_values_twostep,
                    color=approach_colors['twostep'],
                    marker='s',
                    linewidth=3,
                    markersize=8,
                    linestyle='--')
    
    ax_avg_time.fill_between(x_values_twostep, 
                           [max(0, y - std) for y, std in zip(y_values_twostep, y_std_twostep)],
                           [y + std for y, std in zip(y_values_twostep, y_std_twostep)],
                           color=approach_colors['twostep'], alpha=0.2)
    
    ax_avg_time.set_ylabel('Norm. Planning Time', fontsize=12, fontweight='bold')
    ax_avg_time.set_title('Average Across Domains', fontsize=12, fontweight='bold')
    ax_avg_time.grid(True, linestyle='--', alpha=0.7)
    ax_avg_time.set_xticks(range(1, 5))  # Changed to only show up to 4 agents
    ax_avg_time.tick_params(axis='both', labelsize=10)
    
    # Add average execution length plot (bottom right)
    ax_avg_cost = plt.subplot(gs[1, 5])
    ax_avg_cost.set_facecolor('#f8f9fa')  # Add light gray background
    
    # Calculate average normalized execution length for multiagent approach
    y_values_multi = [np.mean(normalized_solution_cost['multiagent'][n]) for n in x_values_multi]
    
    # Calculate average normalized execution length for two-step approach
    y_values_twostep = [np.mean(normalized_solution_cost['twostep'][n]) for n in x_values_twostep]
    y_std_twostep = [np.mean(normalized_solution_cost_std[n]) for n in x_values_twostep]
    
    # Print statistics for normalized execution length
    print("\n=== Normalized Execution Length Statistics ===")
    print("Multiagent approach:")
    for n, value in zip(x_values_multi, y_values_multi):
        print(f"  {n} agents: {value:.4f}")
    
    print("\nTwo-step approach:")
    for n, value, std in zip(x_values_twostep, y_values_twostep, y_std_twostep):
        print(f"  {n} agents: {value:.4f} ± {std:.4f}")
    
    # Plot average execution length
    y_values_multi = [y * 10 for y in y_values_multi]
    y_values_twostep = [y * 10 for y in y_values_twostep]

    ax_avg_cost.plot(x_values_multi, y_values_multi,
                    color=approach_colors['multiagent'],
                    marker='o',
                    linewidth=3,
                    markersize=8,
                    linestyle='-')
    
    ax_avg_cost.plot(x_values_twostep, y_values_twostep,
                    color=approach_colors['twostep'],
                    marker='s',
                    linewidth=3,
                    markersize=8,
                    linestyle='--')
    
    ax_avg_cost.fill_between(x_values_twostep, 
                           [max(0, y - std) for y, std in zip(y_values_twostep, y_std_twostep)],
                           [y + std for y, std in zip(y_values_twostep, y_std_twostep)],
                           color=approach_colors['twostep'], alpha=0.2)
    
    ax_avg_cost.set_ylabel('Norm. Execution Length x10', fontsize=12, fontweight='bold')
    ax_avg_cost.set_xlabel('Number of Agents', fontsize=10, fontweight='bold')
    ax_avg_cost.grid(True, linestyle='--', alpha=0.7)
    ax_avg_cost.set_xticks(range(1, 5))  # Changed to only show up to 4 agents
    ax_avg_cost.tick_params(axis='both', labelsize=10)
    
    # Add a single legend at the top of the figure
    fig = plt.gcf()
    fig.legend(handles=legend_elements, loc='upper center', ncol=2, fontsize=12, 
               frameon=True, bbox_to_anchor=(0.5, 0.98))
    
    plt.suptitle('Planning Time and Execution Length Comparison', 
                 fontsize=14, fontweight='bold', y=1.02)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust the rect to leave space for the legend
    plt.savefig('graphs/grid_layouts/combined_grid.png', dpi=300, bbox_inches='tight')
    plt.close()

# Create individual plots for each domain and metric
for domain in domains:
    create_domain_plot(domain, 'avg_solution_cost', 'Execution Length', 'Execution Lengths')
    create_domain_plot(domain, 'avg_planning_time', 'Planning Time (s)', 'Planning Times')

# Create the combined 2x5 grid layout
create_combined_grid_layout()

# Print tables in markdown format
print("# Planning Results Data Tables\n")

# Print multiagent table
print("## Multiagent PDDL Approach Results\n")
print("| Domain | Agents | Planning Time (s) | Execution Length | Timeouts |")
print("|--------|--------|-------------------|------------------|----------|")

for domain in domains:
    for n in range(1, 6):
        key = f'{domain}-{n}'
        if key in results_dict:
            time = results_dict[key]['avg_planning_time']
            cost = results_dict[key]['avg_solution_cost']
            timeouts = results_dict[key]['timeouts']
            domain_formatted = domain.capitalize()
            print(f"| {domain_formatted} | {n} | {time:.2f} | {cost:.2f} | {timeouts} |")

# Print two-step table
print("\n## Two-Step Approach Results (Average of 3 Runs)\n")
print("| Domain | Agents | Planning Time (s) | Execution Length |")
print("|--------|--------|-------------------|------------------|")

for domain in domains:
    if domain in twostep_data:
        for n in sorted(twostep_data[domain].keys()):
            time = twostep_data[domain][n]['avg_planning_time']
            time_std = twostep_data[domain][n]['std_planning_time']
            cost = twostep_data[domain][n]['avg_solution_cost']
            cost_std = twostep_data[domain][n]['std_solution_cost']
            domain_formatted = domain.capitalize()
            print(f"| {domain_formatted} | {n} | {time:.2f} ± {time_std:.2f} | {cost:.2f} ± {cost_std:.2f} |")

print("\n*Note: For the Two-Step approach, values are presented as mean ± standard deviation from 3 independent runs.*")
