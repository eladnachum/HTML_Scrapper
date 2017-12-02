from costs import costs


print 'hi'
aws_costs_index_url = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json"
costs = costs(aws_costs_index_url)
