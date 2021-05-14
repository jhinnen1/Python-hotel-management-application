#Hotel Management System

#code begins for SQLalchemy database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
#code ends for SQLaclchemy database


class Customer(Base): #a class for customers of the hotel
    def __init__(self, first_name, last_name, state_of_residence):
        self.first_name = first_name
        self.last_name = last_name
        self.state_of_residence = state_of_residence
        
    __tablename__ = "customer" #setting the database table name
    
    id = Column(Integer, primary_key=True) #setting the columns and primary key
    first_name = Column(String)
    last_name = Column(String)
    state_of_residence = Column(String)
        
    def get_full_name(self):
        return self.first_name + " " + self.last_name
    
    def __repr__(self):
        return "Account('{0}', '{1}')".format(self.first_name, self.last_name)
    
    def __str__(self):
        return "First Name: {0} \nLast Name: {1} \nState: {2}".format(self.first_name, self.last_name, self.state_of_residence)


#code for factory design pattern begins here
from abc import ABCMeta, abstractmethod

class HotelRoomBooking(metaclass=ABCMeta): #a class for hotel room bookings
    def __init__(self, room_category, customer):
        self.room_category = room_category
        self.customer = customer
    
    def get_customer(self):
        return self.customer
    
    @abstractmethod
    def get_room_category(self):
        pass
    
    def __str__(self):
        return "{} - {} \n{}".format(self.__class__. __name__, self.room_category, self.get_customer())

class KingRoomBooking(HotelRoomBooking): #a class for room w/one King bed booking
    def get_room_category(self):
        return "King Room"
    
class QueenRoomBooking(HotelRoomBooking): #a class for room w/two Queen beds booking
    def get_room_category(self):
        return "Queen Room"

class HotelRoomBookingFactory(object): #factory that creates an object for each booking
    @classmethod
    def create(cls, name, *args):
        name = name.lower().strip()
        
        if name == "king":
            return KingRoomBooking(*args)
        elif name == "queen":
            return QueenRoomBooking(*args)
#code for factory design pattern ends here    


#code for prototype design pattern begins here
import copy

class Prototype(object): #creates class for the prototype
    def clone(self):
        return copy.deepcopy(self)

class Commission(Prototype): #creates class for commissions paid to travel agencies
    def __init__(self, booking_agency, source, booking_agency_discount, source_discount):
        self.booking_agency = booking_agency
        self.source = source
        self.booking_agency_discount = booking_agency_discount
        self.source_discount = source_discount
        
    def __str__(self):
        return 'Booking Agency: {booking_agency}\nSource: {source}\nDiscounts: {disc1}, {disc2}'.format(booking_agency=self.booking_agency,
   source=self.source,disc1=self.booking_agency_discount,disc2=self.source_discount)                                                                                               
#code for factory design pattern ends here
 
 
#code for singleton design pattern begins here
class HotelManager(object): #creates class for the hotel manager
    _instance = None
    
    def __new__(cls):
        if cls._instance == None:
            cls._instance = object.__new__(cls)
        return cls._instance        
#code for singleton design pattern ends here    

    

def main():
    engine = create_engine('sqlite:///:memory:', echo=False)

    Base.metadata.create_all(engine)
    
    print(" ")
    c1 = Customer("Bob","Myers","MT") #instantiates a customer object
    c2 = Customer("Fred","Gannon","CO")
    c3 = Customer("Dave","Daverson","NY")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    session.add(c1)
    session.add(c2)
    session.add(c3)
    
    newCustomer1 = session.query(Customer).filter_by(last_name="Myers").first()
    print(newCustomer1)
    print(" ")
    
    c1.state_of_residence = "OK"
    print(session.dirty)
    session.commit()
    print(" ")
    print(c1)
    print(" ")
    
    print(c1.id)
    print(" ")
    
    session.add_all([
        Customer(first_name="Todd",last_name="Rogers",state_of_residence="AR"),
        Customer(first_name="Charity",last_name="Smith",state_of_residence="FL")])
    session.commit()
    
    for row in session.query(Customer).all():
        print(row.last_name, row.state_of_residence)
        
    print(" ")
    print("*************")            
    
  
    f1 = HotelRoomBookingFactory() #instantiates a factory object
    
    k1 = f1.create("king", "new customer", c1) #instantiates a king room reservation object
    print(k1)
    print(" ")
    
    q1 = f1.create("queen", "past customer", c2) #instantiates a queen room reservation object
    print(q1)
    print(" ")
    
    k1 = f1.create("king", "new customer", c3)
    print(k1)
    print(" ")
    
    print("*************")
    
    c1 = Commission("Booking.com","TripAdvisor",0.95,0.75) #instantiates a commission object
    print(c1)
    print(" ")
    c2 = c1.clone() #instantiates a new commission object as a clone
    c2.booking_agency = "Hotels.com"
    c2.booking_agency_discount = 0.90
    print(c2)
    print(" ")
    c3 = c1.clone()
    c3.booking_agency = "Expedia.com"
    c3.booking_agency_discount = 0.80
    print(c3)
    print(" ")
    
    print("**************")
    
    hm1 = HotelManager() #instantiates a hotel manager object
    hm2 = HotelManager()
    print(hm1 == hm2)
    print(" ")
    
    print("**************")
   
 
    
main()
