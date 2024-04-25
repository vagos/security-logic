class Customer:
    def __init__(self, name, bid_limit=None):
        self.name = name #{Customer :{Customer,AuctionHouse}}
        self.bid_limit = bid_limit  #{Customer : {Customer,AuctionHouse}}
    


class AuctionHouse:
    def __init__(self, name):
        self.name = name #{AuctionHouse : {⊥}}
        self.customers = {} #{AuctionHouse : AuctionHouse}
        # Instead of holding auction house objects, we use a mapping of names to verification methods
        self.trusted_auction_houses = {} #{AuctionHouse : {AuctionHouse}}

    def add_customer(self, name, bid_limit=None):
        #if_acts_for(add_customer,Customer)
        #customer_info := declassify(Customer(),{AuctionHouse})
        customer_info = Customer(name, bid_limit)
        self.customers[name] = customer_info  # self.customers[name] : {AuctionHouse : AuctionHouse}

    def set_auction_house_trust(self, auction_house_name, verification_method):
        self.trusted_auction_houses[auction_house_name] = verification_method 
        #verification_method : {AuctionHouse' : {AuctionHouse'}} all the customers (and their bid_limit) owned by other trusted auction houses used as the reference
        # auction_house_name : {AuctionHouse : {⊥}}, everyone can read auction house name
        # we use customer's bid limit as verification method, the bid limit : {AuctionHouse : {Customer,AuctionHouse}}, so auction house can read customer's bid limit


    def verify_customer_bid_limit(self, customer_name):
        # customer_name : {Customer : {Customer,AuctionHouse}}
        # self.customers[customer_name].bid_limit : {AuctionHouse' : {Customer,AuctionHouse'}}
        # This step involves some auction house reading customers' bid_limit from other trusted auction houses, which is declassified in the main method.
        if customer_name in self.customers:
            return self.customers[customer_name].bid_limit #{AuctionHouse' : {AuctionHouse'}}
        else:
            return None # {AuctionHouse' : {AuctionHouse'}}

    def accept_customer_with_reference(self, customer_name, reference_auction_house_name):
        # customer_name : {Customer : {Customer,AuctionHouse}}
        # reference_auction_house_name : {AuctionHouse' : {AuctionHouse'}}
        # self.trusted_auction_houses : {AuctionHouse' : {AuctionHouse'}}
        # verification_method : {AuctionHouse : {AuctionHouse}}
        # bid_limit : {AuctionHouse' : {Customer,AuctionHouse'}}
        if reference_auction_house_name in self.trusted_auction_houses:
            verification_method = self.trusted_auction_houses[reference_auction_house_name]
            # auction house' is any other auction house that is verifying a customer based on the reference of trusted auction houses
            # verification_method : {AuctionHouse' : {AuctionHouse'}}
            bid_limit = verification_method(customer_name)
            # bid_limit is declassfied for auction house' in the verification phase in the main method.
            if bid_limit is not None:
                self.add_customer(customer_name, bid_limit)
                # auction house' stores the customer's name and bid limit
                print(f"{customer_name} has been accepted with a bid limit of {bid_limit} based on their status from {reference_auction_house_name}.")
            else:
                print(f"{customer_name} is not a customer of {reference_auction_house_name}.")
        else:
            print(f"{reference_auction_house_name} is not a trusted auction house for {self.name}.")

    def print_customers(self):
        for customer in self.customers.values():
            print(f"Customer: {customer.name}, Bid Limit: {customer.bid_limit}") 
            # customer.name : {AuctionHouse : {AuctionHouse}}, customer.bid_limit : {AuctionHouse : {AuctionHouse}}
       

def main():

    # Setup

    auction_house_a = AuctionHouse("AuctionHouseA") # {AuctionHouse : {Customer,AuctionHouse}}
    auction_house_b = AuctionHouse("AuctionHouseB") # {AuctionHouse : {Customer,AuctionHouse}}
    auction_house_c = AuctionHouse("AuctionHouseC") # {AuctionHouse : {Customer,AuctionHouse}}

    auction_house_a.add_customer("Alice", 500) 
    #customer name : {Customer : {Customer,AuctionHouse}},customer bid_limit : {Customer : {Customer,AuctionHouse}} 

    # solved for now : can explain the report, and then delete the comment. 
    # With regard to the trust auction house, each auction house trusts the other auction house. 
    # Although the auction house name is public, the verification method (bid limit) is private.
    # And essentially, the auction house only knows their owned customer bid limit. therefore, we may also consider the declassification of bid limit from other auction houses
    
    # B trusts A by specifying A's verification method
    #if_acts_for(main,auction_house_a)
    #verification := declassify(auction_house_a,{auction_house_n (these are any other auction houses)})
    verificaition = auction_house_a.verify_customer_bid_limit
    auction_house_b.set_auction_house_trust("AuctionHouseA", verificaition) # {AuctionHouse' : {AuctionHouse'}} auction house prime means other auction houses e.g. auction house b

    # C trusts B in a similar manner
    auction_house_c.set_auction_house_trust("AuctionHouseB", auction_house_b.verify_customer_bid_limit) # {AuctionHouse' : {AuctionHouse'}}

    # Verifying Alice's bid limit through references
    # The following method is run by auction house prime
    # auction house b accepts the auction house a's customer, Alice, with the reference of auction house a
    auction_house_b.accept_customer_with_reference("Alice", "AuctionHouseA") 
    auction_house_c.accept_customer_with_reference("Alice", "AuctionHouseB") 
    auction_house_b.accept_customer_with_reference("Bob", "AuctionHouseA")

    # auction house prints their customer's reference
    auction_house_b.print_customers()   # {AuctionHouse : {AuctionHouse}}
    auction_house_c.print_customers()   # {AuctionHouse : {AuctionHouse}}

main()


