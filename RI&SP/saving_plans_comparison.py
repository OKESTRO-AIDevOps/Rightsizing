import boto3

def get_aws_pricing(service_code, region):
    pricing = boto3.client('pricing', region_name=region)
    response = pricing.get_products(
        ServiceCode=service_code,
        Filters=[
            {
                'Type': 'TERM_MATCH',
                'Field': 'location',
                'Value': region,
            },
        ],
    )
    return response

def get_savings_plans_prices(region):
    service_code = 'AmazonEC2'  # AWS service code for EC2 instances
    response = get_aws_pricing(service_code, region)
    
    # Extract Savings Plans pricing details
    savings_plans_prices = {}
    for product in response['PriceList']:
        attributes = product['Product']['Attributes']
        if 'savingsPlan' in attributes:
            instance_type = attributes['instanceType']
            savings_plans_prices[instance_type] = {
                'price_per_hour': float(attributes['priceDimensions'].values()[0]['pricePerUnit']['USD']),
            }
    
    return savings_plans_prices

def get_on_demand_instance_prices(region):
    service_code = 'AmazonEC2'  # AWS service code for EC2 instances
    response = get_aws_pricing(service_code, region)
    
    # Extract on-demand instance pricing details
    on_demand_instance_prices = {}
    for product in response['PriceList']:
        attributes = product['Product']['Attributes']
        if 'locationType' in attributes and attributes['locationType'] == 'AWS Region':
            instance_type = attributes['instanceType']
            on_demand_instance_prices[instance_type] = {
                'price_per_hour': float(attributes['priceDimensions'].values()[0]['pricePerUnit']['USD']),
            }
    
    return on_demand_instance_prices

def main():
    region = 'region'  # Replace with your desired AWS region
    
    savings_plans_prices = get_savings_plans_prices(region)
    on_demand_instance_prices = get_on_demand_instance_prices(region)
    
    print("Savings Plans Prices:")
    for instance_type, details in savings_plans_prices.items():
        print(f"Instance Type: {instance_type}, Price per Hour: ${details['price_per_hour']:.4f}")
    
    print("\nOn-Demand Instance Prices:")
    for instance_type, details in on_demand_instance_prices.items():
        print(f"Instance Type: {instance_type}, Price per Hour: ${details['price_per_hour']:.4f}")

if __name__ == '__main__':
    main()