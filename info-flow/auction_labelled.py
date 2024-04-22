# L_C : live_customer
class Customer():
    def __init__(self, name, max_bid, commisioned=True):
        self.name = name  # {C:{C,A}}
        self.max_bid = max_bid  # {C:{C,A}}
        self.commisioned = commisioned  # {C:{C,A}}
        self.current_bid = 0  # Not used right now #{C:{A, L_C}}
        self.out = False
# annotate


class AuctionHouse():
    def __init__(self, name, bid_step=50):
        self.name = name  # {A:{⊥}}
        self.customers = []  # {C:{A}}
        self.current_bid = 0  # {A(on behalf of the comissioned customer?):{A, L_C}}
        self.bid_step = bid_step  # {A:{A,L_C}}


def doLiveCustomerBid(customer, auction_house):
    # live_customer_name(owner) : {L_C: {L_C, A}}
    # the set of readers for the owner "auction house" already declared
    if customer.max_bid >= auction_house.current_bid + auction_house.bid_step:
        # implicit flow: infoFlow from customer.max_bid to auction_house.current_bid
        # in theory: max_bid :: {C:{}} == owner is customer and read by no one
        # however:
        auction_house.current_bid += auction_house.bid_step
        # there is a reader in violation of the set
        # declassification required?
        print(f"{customer.name} bids {auction_house.current_bid} Units")
        #to prevent the violation of iflow :
        #first declare : i:int{⊥} := 0 #not sure about this
        #if the conditional statement is true:
        #if_acts_for(doLiveCustomerBid, customer) #doLiveCustomer program acts on behalf of the live customer
        #i:= declassify(customer.max_bid, {auction_house})
        return True
    return False


def doCommissionedCustomerBid(customer, auction_house):
    if customer.commisioned and customer.max_bid >= auction_house.current_bid + auction_house.bid_step:
        # customer.commisioned = {C:{A,C}}
        # commisioned_customer.max_bid = {C:A,C}
        # ^ the same problem of implicit flow ^
        # current_bid : { A: {A, C_live}}
        # the value of the above depends on the condtional statement with data that violates the set of readers set initially
        print(f"Auction house bids for {customer.name}: {auction_house.current_bid} Units")
        return True
    return False


def simulate_auction(auction_house):
    winner = auction_house.customers[0]
    # winner : {A:{winning_customer}}
    while True:
        next_possible_bid = auction_house.current_bid + auction_house.bid_step
        # next_possible_bid : {A:{}} #no one should be able to read this?
        # except in the case when auction house is bidding on behalf of commissioned customer:
        # next_possible_bid (if commissioned customer): {A:{A}}
        # Determine if any bidder can still bid
        potential_bidders = [c for c in auction_house.customers if c.max_bid >= next_possible_bid]
        # what if c.max_bid is from live customer? isn't the auction house not allowed to read that?
        #live_bid :int {⊥}
        #if_acts_for(simulate_auction, live_customer)
            #live_bid := declassify(live_customer.max_bid, {auctionHouse?})

        if not potential_bidders:
            print("No bidder can continue.")
            break

        found_winner = len([c for c in auction_house.customers if c.out is False and c.max_bid >= auction_house.current_bid]) == 1
        # found_winner : {A:{A}}
        # ^ value depends on data that does not have any readers i.e.:
        # in case c.max_bid is from a live customer

        # Live bidders will bid only if there's competition
        if not found_winner:
            for customer in ([c for c in potential_bidders if not c.commisioned]):
                # all the customers that are not commisioned i.e. live
                # "customer" variable here: {A:{A}} owned and read by auction house
                if doLiveCustomerBid(customer, auction_house):
                    winner = customer
                    # winner : {A:{A, C_winner}}

        # Commissioned bidding
        for customer in sorted(potential_bidders, key=lambda x: x.max_bid, reverse=True):
            # customer : {A:{A}}
            # potential bidders : {A:{A}}
            raisesBid = doCommissionedCustomerBid(customer, auction_house) 
            if raisesBid:
                # declassify(raisesBid, {⊥})
                auction_house.current_bid += auction_house.bid_step
                winner = customer
                # winner : {A:{A, C_winner}}  # or: {A:{A}}
                break

        if found_winner:
            # found_winner : {A:{A}}
            print("going once ... going twice ... sold!")
            print(f"The item is sold for {auction_house.current_bid} Units!")
            # if found_winner, winning_bid is auction_house.current_bid here : {⊥} read by everyone
            print(f"The winner is {winner.name}")
            # winner.name : {A:{⊥}}
            # however
            # we labelled the set as { A: {C_winner } }
            break

def main():

    auction_house = AuctionHouse("Units Auction House")
    bidder_a = Customer("Bidder A", 500, commisioned=True)
    bidder_b = Customer("Bidder B", 700, commisioned=True)
    bidder_c = Customer("Bidder C", 1000, commisioned=False)
    # bidder_d = Customer("Bidder D", 2000, commisioned=False)  # Another live bidder for the example
    auction_house.customers.extend([bidder_a, bidder_b, bidder_c])  # max_bid by from live customer is read by the auction house

    auction_house.current_bid = 500
    print(f"Starting the auction at {auction_house.current_bid} Units!")

    simulate_auction(auction_house)


main()
