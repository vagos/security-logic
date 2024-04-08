class Customer:
    def __init__(self, name, bid_limit=100):
        self.name = name
        self.bid_limit = bid_limit
        self.reference = ""


class AuctionHouse:
    def __init__(self, name):
        self.name = name
        self.customers = {}
        # Instead of holding auction house objects, we use a mapping of names to verification methods
        self.trusted_auction_houses = {}

    def add_customer(self, name, bid_limit=100):
        self.customers[name] = Customer(name, bid_limit)

    def set_auction_house_trust(self, auction_house_name, verification_method):
        self.trusted_auction_houses[auction_house_name] = verification_method

    def verify_customer_bid_limit(self, customer_name):
        if customer_name in self.customers:
            return self.customers[customer_name].bid_limit
        else:
            return None

    def accept_customer_with_reference(self, customer_name, reference_auction_house_name):
        if reference_auction_house_name in self.trusted_auction_houses:
            verification_method = self.trusted_auction_houses[reference_auction_house_name]
            bid_limit = verification_method(customer_name)
            if bid_limit is not None:
                self.add_customer(customer_name, bid_limit)
                print(f"{customer_name} has been accepted with a bid limit of {bid_limit} based on their status from {reference_auction_house_name}.")
            else:
                print(f"{customer_name} is not a customer of {reference_auction_house_name}.")
        else:
            print(f"{reference_auction_house_name} is not a trusted auction house for {self.name}.")

    def print_customers(self):
        for customer in self.customers.values():
            print(f"Customer: {customer.name}, Bid Limit: {customer.bid_limit}")


def main():

    # Setup
    auction_house_a = AuctionHouse("AuctionHouseA")
    auction_house_b = AuctionHouse("AuctionHouseB")
    auction_house_c = AuctionHouse("AuctionHouseC")

    auction_house_a.add_customer("Alice", 500)

    # B trusts A by specifying A's verification method
    auction_house_b.set_auction_house_trust("AuctionHouseA", auction_house_a.verify_customer_bid_limit)

    # C trusts B in a similar manner
    auction_house_c.set_auction_house_trust("AuctionHouseB", auction_house_b.verify_customer_bid_limit)

    # Verifying Alice's bid limit through references

    # This is run by the customer
    auction_house_b.accept_customer_with_reference("Alice", "AuctionHouseA")
    auction_house_c.accept_customer_with_reference("Alice", "AuctionHouseB")
    auction_house_b.accept_customer_with_reference("Bob", "AuctionHouseA")

    auction_house_b.print_customers()
    auction_house_c.print_customers()


main()
