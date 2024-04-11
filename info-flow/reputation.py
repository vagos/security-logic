class Security_Label:
    def __init__(self):
        self.label = ""
        self.owner = [] 
        self.reader = []
    
    def add_owner(self, owner):
        self.owner.append(owner)
    
    def add_reader(self, reader):
        self.reader.append(reader)
    
    def set_sec_label(self):
        ownset = ' '.join(self.owner)
        readset = ' '.join(self.reader)
        label = f"{ownset} : {readset}"
        self.label = label
    def get_sec_label(self):
        return f"{{{self.label}}}"

class Customer:
    def __init__(self, name, bid_limit=100):
        self.name = name #{Customer : AuctionHouse}
        self.bid_limit = bid_limit #{AuctionHouse : {Customer,AuctionHouse}}
        self.reference = "" #{AuctionHouse : {Customer,AuctionHouse}}


class AuctionHouse:
    def __init__(self, name):
        self.name = name #{AuctionHouse : {AuctionHouse,Customer}}
        self.customers = {} #{AuctionHouse : AuctionHouse}
        # Instead of holding auction house objects, we use a mapping of names to verification methods
        self.trusted_auction_houses = {} #{AuctionHouse : {AuctionHouse}}

    def add_customer(self, name, bid_limit=100):
        self.customers[name] = Customer(name, bid_limit) #{Customer : AuctionHouse}.
        # "name" : The name of customer, auctionhouse can read. 
        # "bid_limit" : auctionhouse is owner.

    def set_auction_house_trust(self, auction_house_name, verification_method):
        self.trusted_auction_houses[auction_house_name] = verification_method #{AuctionHouse : {AuctionHouse}}

    def verify_customer_bid_limit(self, customer_name):
        # customer_name : {Customer : AuctionHouse}
        # self.customers[customer_name].bid_limit : {AuctionHouse : {Customer,AuctionHouse}}
        if customer_name in self.customers:
            return self.customers[customer_name].bid_limit #{AuctionHouse : {Customer,AuctionHouse}}
        else:
            return None #{⊥}

    def accept_customer_with_reference(self, customer_name, reference_auction_house_name):
        # customer_name : {Customer : AuctionHouse}
        # reference_auction_house_name : {AuctionHouse : {AuctionHouse}}
        # trusted_auction_houses : {AuctionHouse : {AuctionHouse}}
        # verification_method : {AuctionHouse : {AuctionHouse}}
        # bid_limit : {AuctionHouse : {Customer,AuctionHouse}}
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
            print(f"Customer: {customer.name}, Bid Limit: {customer.bid_limit}") # customer.name : {Customer : AuctionHouse}, customer.bid_limit : {AuctionHouse : {Customer,AuctionHouse}}


def main():

    # Setup
    auction_house_a = AuctionHouse("AuctionHouseA") # {AuctionHouse : {AuctionHouse,Customer}}
    auction_house_b = AuctionHouse("AuctionHouseB") # {AuctionHouse : {AuctionHouse,Customer}}
    auction_house_c = AuctionHouse("AuctionHouseC") # {AuctionHouse : {AuctionHouse,Customer}}

    auction_house_a.add_customer("Alice", 500) # {Customer : AuctionHouse}

    # B trusts A by specifying A's verification method
    auction_house_b.set_auction_house_trust("AuctionHouseA", auction_house_a.verify_customer_bid_limit) # {AuctionHouse : {AuctionHouse}}

    # C trusts B in a similar manner
    auction_house_c.set_auction_house_trust("AuctionHouseB", auction_house_b.verify_customer_bid_limit) # {AuctionHouse : {AuctionHouse}}

    # Verifying Alice's bid limit through references

    # This is run by the customer
    auction_house_b.accept_customer_with_reference("Alice", "AuctionHouseA") #"Alice" : {Customer : AuctionHouse}, "AuctionHouseA" : {AuctionHouse : {AuctionHouse}}
    auction_house_c.accept_customer_with_reference("Alice", "AuctionHouseB") #"Alice" : {Customer : AuctionHouse}, "AuctionHouseB" : {AuctionHouse : {AuctionHouse}}
    auction_house_b.accept_customer_with_reference("Bob", "AuctionHouseA")   #"Bob" : {Customer : AuctionHouse}, "AuctionHouseA" : {AuctionHouse : {AuctionHouse}}

    auction_house_b.print_customers()   # {AuctionHouse : {AuctionHouse}}
    auction_house_c.print_customers()   # {AuctionHouse : {AuctionHouse}}

    # Security Label testing
    sc = Security_Label()
    sc.add_owner("AuctionHouseA")
    sc.add_reader("AuctionHouseB")
    sc.set_sec_label()
    label = sc.get_sec_label()
    print("Variable : sc, Label : ", label)

main()
