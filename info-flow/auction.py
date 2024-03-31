class Customer():
    def __init__(self, name, max_bid, commisioned=True):
        self.name = name
        self.max_bid = max_bid
        self.commisioned = commisioned
        self.current_bid = 0  # Not used right now
        self.out = False


class AuctionHouse():
    def __init__(self, name, bid_step=50):
        self.name = name
        self.customers = []
        self.current_bid = 0
        self.bid_step = bid_step


auction_house = AuctionHouse("Units Auction House")
bidder_a = Customer("Bidder A", 500, commisioned=True)
bidder_b = Customer("Bidder B", 700, commisioned=True)
bidder_c = Customer("Bidder C", 1000, commisioned=False)
bidder_d = Customer("Bidder D", 2000, commisioned=False)  # Another live bidder for the example
auction_house.customers.extend([bidder_a, bidder_b, bidder_c])

auction_house.current_bid = 500
print(f"Starting the auction at {auction_house.current_bid} Units!")


def doLiveCustomerBid(customer, auction_house):
    if customer.max_bid >= auction_house.current_bid + auction_house.bid_step:
        auction_house.current_bid += auction_house.bid_step
        print(f"{customer.name} bids {auction_house.current_bid} Units")
        return True

    return False


def doCommissionedCustomerBid(customer, auction_house):
    if customer.commisioned and customer.max_bid >= auction_house.current_bid + auction_house.bid_step:
        auction_house.current_bid += auction_house.bid_step
        print(f"Auction house bids for {customer.name}: {auction_house.current_bid} Units")
        return True

    return False


def simulate_auction(auction_house):
    winner = auction_house.customers[0]
    while True:
        next_possible_bid = auction_house.current_bid + auction_house.bid_step
        # Determine if any bidder can still bid
        potential_bidders = [c for c in auction_house.customers if c.max_bid >= next_possible_bid]

        if not potential_bidders:
            print("No bidder can continue.")
            break

        found_winner = len([c for c in auction_house.customers if c.out is False and c.max_bid >= auction_house.current_bid]) == 1

        # Live bidders will bid only if there's competition
        if not found_winner:
            for customer in ([c for c in potential_bidders if not c.commisioned]):
                if doLiveCustomerBid(customer, auction_house):
                    winner = customer

        # Commissioned bidding
        for customer in sorted(potential_bidders, key=lambda x: x.max_bid, reverse=True):
            if doCommissionedCustomerBid(customer, auction_house):
                winner = customer
                break

        if found_winner:
            print("going once ... going twice ... sold!")
            print(f"The item is sold for {auction_house.current_bid} Units!")
            print(f"The winner is {winner.name}")
            break


simulate_auction(auction_house)
