class Customer():
    def __init__(self, name, max_bid, commisioned=True):
        self.name = name  # {C:{}}
        self.max_bid = max_bid  # {C:{}}
        self.commisioned = commisioned  # {C:{}}
        #self.current_bid = 0  # Not used right now #{C:{A, C}}
        self.out = False #{A:{A}}

class AuctionHouse():
    def __init__(self, name, bid_step=50):
        self.name = name  # {A:{⊥}}
        self.customers = []  # {A:{A}}
        self.current_bid = 0  # {A(on behalf of the comissioned customer?):{A, C}}
        self.bid_step = bid_step  # {A:{⊥}}


def doesLiveCustomerRaiseBid(customer, auction_house):
    # returns customerChoice: { C : {⊥}} 
    customerChoice = False
    # Get the data from the Live Customer
    # if_acts_for(doesLiveCustomerRaiseBid, {C})
    # customerChoice := declassify(customerChoice, {C:{⊥}})
    return customerChoice # { C : {⊥} }


def doesCommisionedCustomerRaiseBid(customer, auction_house):
    doesRaiseBid=False
    if customer.commisioned and customer.max_bid >= auction_house.current_bid + auction_house.bid_step:
        # customer.commisioned = {A:{A}}
        # commisioned_customer.max_bid = {C:A,C}
        # current_bid : { A: {A, C_live}}
        print(f"Auction house bids for {customer.name}: {auction_house.current_bid} Units")
        doesRaiseBid = True
    return doesRaiseBid

def doesRaiseBid(customer, auction_house):
    if customer.commisioned:
        choice = doesCommisionedCustomerRaiseBid(customer, auction_house)
    else:
        choice = doesLiveCustomerRaiseBid(customer, auction_house)
    
    return choice


def simulate_auction(auction_house):
    winner = auction_house.customers[0]
    # winner : {A:{}}
    while True:
        next_possible_bid = auction_house.current_bid + auction_house.bid_step
        # next_possible_bid : {A:{}} 
        # Determine if any bidder can still bid
        potential_bidders = [c for c in auction_house.customers if doesRaiseBid(c, auction_house)]
        #potential_bidders: {A:{A}, C{⊥}} 
        #effective_readers = {A}

        if not potential_bidders:
            print("No bidder can continue.")
            break

        for customer in potential_bidders:

            raisesBid = doesRaiseBid(customer, auction_house) 
            if raisesBid:
            # raisesBid: {C:{⊥}}
                auction_house.current_bid += auction_house.bid_step
                winner = customer
            #customer:{{A:{A}, C{⊥}}}
            #customer := potential_bidders
            # winner := customer
                break

        found_winner = len([c for c in auction_house.customers if c.out is False and doesRaiseBid(c, auction_house)]) == 1
        # found_winner : {C:{⊥}, A:{A}}
        #doesRaiseBid(C:{⊥}) U c.out(A:{A}): {C:{⊥}, A{A}}
        #effective readers : {A} #the intersection of readers above^

        if found_winner:
            # found_winner : {A:{A}}
            print("going once ... going twice ... sold!")
            print(f"The item is sold for {auction_house.current_bid} Units!")
            #if_acts_for(simulate_auction, {A,C})
            #winner := declassify(winner,{⊥})
            print(f"The winner is {winner.name}")
            # winner.name : {A:{⊥}}
            #the winner is declassified because it was owned by both the auction house and customer. The effective reader was only the auction house
            break
            

auction_house = AuctionHouse("Units Auction House")

def signup():

    bidder_a = Customer("Bidder A", 500, commisioned=True)
    bidder_b = Customer("Bidder B", 700, commisioned=True)
    bidder_c = Customer("Bidder C", 1000, commisioned=False)
    #bidder_n : {C: {}}
    # Restriction : bidder_n : {C:{}, A:{}}
    # effective readers: {}
    #if_acts_for(singup, {C, A}):
        #bidder_n := declassify(bidder_n, {C:{A}, A: {A}})
    # effective readers: {A}
    auction_house.customers.extend([bidder_a, bidder_b, bidder_c])  

    auction_house.current_bid = 500
    print(f"Starting the auction at {auction_house.current_bid} Units!")



signup()
simulate_auction(auction_house)
