import boto3
import matplotlib.pyplot as plt
import pandas as pd
from docx import Document
from docx.shared import Inches
from datetime import datetime, timedelta

# AWS Cost Explorer client
client = boto3.client('ce')

# Helper function to get the start and end dates for the past 3 months
def get_date_range(months):
    end = datetime.today().replace(day=1)  # First day of current month
    start = (end - timedelta(days=months*30)).replace(day=1)  # First day 3 months ago
    return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')

# Get cost data for the last 3 months, grouped by service
def get_cost_data():
    start_date, end_date = get_date_range(3)
    response = client.get_cost_and_usage(
        TimePeriod={'Start': start_date, 'End': end_date},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )
    return response['ResultsByTime']

# Process and compare costs over the months
def process_cost_data():
    data = get_cost_data()
    service_costs = {}
    monthly_totals = {}

    # Parse the response and accumulate costs for each service
    for month_data in data:
        month = month_data['TimePeriod']['Start']
        monthly_total = 0
        
        for group in month_data['Groups']:
            service = group['Keys'][0]
            cost = float(group['Metrics']['UnblendedCost']['Amount'])
            monthly_total += cost
            
            if service not in service_costs:
                service_costs[service] = [0] * len(data)  # Create a list with 0s for each month
            service_costs[service][data.index(month_data)] = cost
        
        monthly_totals[month] = monthly_total

    # Identify top 9 services
    sorted_services = sorted(service_costs.items(), key=lambda x: sum(x[1]), reverse=True)
    top_services = dict(sorted_services[:9])  # Get top 9 services
    other_services_total = [sum(x) for x in zip(*[costs for service, costs in sorted_services[9:]])]

    # Colors for the graph
    colors = plt.colormaps['tab20'](range(len(top_services) + 1))

    # Plot total costs for top 9 services
    plt.figure(figsize=(12, 6))
    bottom = [0] * len(data)  # To stack the bars on top of each other
    months = [month_data['TimePeriod']['Start'] for month_data in data]

    for i, (service, costs) in enumerate(top_services.items()):
        plt.bar(months, costs, bottom=bottom, color=colors[i], label=service)
        bottom = [a + b for a, b in zip(bottom, costs)]  # Accumulate bottom for stacking

    # Plot the "Others" category
    if other_services_total:
        plt.bar(months, other_services_total, bottom=bottom, color=colors[len(top_services)], label='Others')

    plt.xlabel('Month')
    plt.ylabel('Total Cost (USD)')
    plt.title('Monthly Total Costs')
    
    # Move the legend below the plot
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3)  # Move the legend below the plot

    plt.grid(True)
    plt.tight_layout()
    plt.savefig('monthly_total_costs_fixed.png')
    plt.show()

if __name__ == "__main__":
    process_cost_data()
