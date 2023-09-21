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

def get_reserved_instance_prices(region):
    service_code = 'AmazonEC2'
    response = get_aws_pricing(service_code, region)
    
    reserved_instance_prices = {}
    for product in response['PriceList']:
        attributes = product['Product']['Attributes']
        if 'reservedInstance' in attributes:
            instance_type = attributes['instanceType']
            offering_class = attributes['offeringClass']
            reserved_instance_prices[instance_type] = {
                'offering_class': offering_class,
                'price_per_hour': float(attributes['priceDimensions'].values()[0]['pricePerUnit']['USD']),
            }
    
    return reserved_instance_prices

def get_on_demand_instance_prices(region):
    service_code = 'AmazonEC2'
    response = get_aws_pricing(service_code, region)
    
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
    region = 'region'
    
    reserved_instance_prices = get_reserved_instance_prices(region)
    on_demand_instance_prices = get_on_demand_instance_prices(region)
    
    print("Reserved Instance Prices:")
    for instance_type, details in reserved_instance_prices.items():
        print(f"Instance Type: {instance_type}, Offering Class: {details['offering_class']}, Price per Hour: ${details['price_per_hour']:.4f}")
    
    print("\nOn-Demand Instance Prices:")
    for instance_type, details in on_demand_instance_prices.items():
        print(f"Instance Type: {instance_type}, Price per Hour: ${details['price_per_hour']:.4f}")

if __name__ == '__main__':
    main()