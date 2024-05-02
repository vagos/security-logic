class Customer:
    def __init__(self, name, bid_limit=None):
        self.name = name # { Ao: {Ao} } # Customer name has already been registered with the other AuctionHouse
        self.bid_limit = bid_limit # { Ao: {Ao} } # This is written to from the original auction house.

    def update_bid_limit(self, new_limit):
        # new_limit: { A: {A} }
        self.bid_limit = new_limit
        print(f"{self.name}'s bid limit updated to {self.bid_limit}")

class AuctionHouse:
    def __init__(self, name):
        self.name = name # { Ai: {⊥} }
        self.customers = {}  # { Ai: {Ai} } # Stores customer objects with their name as the key
        self.starting_bid_limit = 100 # { Ai: {Ai} } # Default bid limit for new customers

    def signup(self, name, bid_limit=None):
        # name: { Ao: {Ao} }
        # bid_limit: { Ao: {Ao} }
        customer = Customer(name, bid_limit)
        self.register_customer(customer)
        return customer

    def register_customer(self, customer):

    def import_customer(self, customer):
        # customer: { Ao: {Ai} }
        self.customers[customer.name] = customer
        if customer.bid_limit is None:  # Set a default limit for first-time customers
            customer.bid_limit = self.starting_bid_limit  # Default bid limit, can be changed as needed
        print(f"Customer {customer.name} registered with a bid limit of {customer.bid_limit}")


def addCustomer(customer, ah, reference_ah):
    # customer: { Ao: {Ao} }
    # ah: { Ai: {Ai} }
    # reference_ah: { Ao: {Ao} }

    # if_acts_for(addCustomer, reference_ah)
    # customer := endorse(customer, {}) # Everyone trusts the customer
    # restriction: customer { Ai: {} }
    # if_acts_for(addCustomer, ah)
    # customer := endorse(customer, {Ai: {Ai})
    reference_ah.import_customer(customer)

ah_B = AuctionHouse("AuctionHouseB") # { Ai: {Ai} }
ah_C = AuctionHouse("AuctionHouseC") # { Ao: {Ao} }

customer_A = ah_B.signup("Alice", 300) # { Ao: {Ao} }

# restriction: ah_B { Ao: {Ao}, Ai: {} }
# if_acts_for(main, {Ao, Ai})
# ah_c := endorse(ah_c, {Ao: {Ao, Ai})
# restriction: ah_C { Ao: {Ai} }
addCustomer(customer_A, ah_C, ah_B)
