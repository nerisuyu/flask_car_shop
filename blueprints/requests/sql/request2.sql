SELECT nameCustomer FROM carshop.customer as Name where to_days(curdate()) - to_days(dateCustomer) < '$days'
