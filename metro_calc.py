import wmataAPI8 as wmata
import numpy as np

  
'''
*************** METRO CALC *************** 
'''
def metroCalc(START_NAME, END_NAME, DAYS_OF_METRO, SUBSIDY):
    PASS_FARES = list(np.linspace(2.00, 6.00, 17))

    api = wmata.wmataAPI('0d79b57328d54a1688294c01d9402f50')
    
    def get_cost(price_point, fare, subsidy = 1, days_using_metro=30):
        pass_cost = subsidy*2*price_point*18 
        if fare-price_point > 0: 
            per_trip_cost = fare-price_point
        else:
            per_trip_cost = 0
            
        additional_days = max(0, days_using_metro-18)
        additional_cost = 2*days_using_metro*per_trip_cost
        return (pass_cost + additional_cost, pass_cost, additional_cost)
       
    START_STATION = api.name_to_code(START_NAME)
    END_STATION = api.name_to_code(END_NAME) 
    fare = api.__s2s__(START_STATION, END_STATION).peak_fare
    
    cost = [get_cost(p, fare, SUBSIDY, DAYS_OF_METRO)[0] for p in PASS_FARES]
    cost_full = [get_cost(p, fare, SUBSIDY, DAYS_OF_METRO) for p in PASS_FARES]
    min_index = cost.index(min(cost))
    no_pass_cost = 2*DAYS_OF_METRO*fare
    
    best_pass = PASS_FARES[min_index]
    pass_cost = cost_full[min_index][1]
    add_cost = cost_full[min_index][2]
    total_cost = pass_cost/SUBSIDY + add_cost
    subsidized_cost = pass_cost + add_cost
    savings = max(0, no_pass_cost - total_cost)
    days_not_covered = max(0, DAYS_OF_METRO - 18)
    
    if subsidized_cost > no_pass_cost:
        best_pass = 0
    
    print("|************************|" \
        "\n|    METRO CALCULATOR    |" \
        "\n|************************|")
    print("***choo choo***")
    print("BASED OFF OF DAILY ROUTE FROM %s TO %s\n" % (START_NAME, END_NAME))
    print ("BEST PASS PRICE POINT: $%.2f\n" \
           "BASE FARE: $%.2f\n" \
           "\n..TOTAL COST: $%.2f" \
           "\n..SUBSIDIZED COST: $%.2f" \
           "\n......PASS COST: $%.2f" \
           "\n......ADDT. COST: $%.2f" \
           "\n..NO PASS COST: $%.2f" \
           "\n......SAVINGS: $%.2f" \
           "\n...DAYS USING METRO: %i" \
           "\n......DAYS NOT COVERED BY PASS: %i" \
           % (best_pass, fare, total_cost, subsidized_cost, pass_cost, add_cost,
              no_pass_cost, savings, DAYS_OF_METRO, days_not_covered))

