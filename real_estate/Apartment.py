class Apartment(object):
    """An  apartment for sale
        Attributes:
            url:
            address: address of the aparatment
            neighborhood:
            price:
            size: in square-feet
            floor:
            total_floors: total floors in the building
            rooms: number of rooms
            agent: real estate agent or private
            contact_name:
            contact_phone:
            details:
        """
    def __init__(self, url):
        self.url = url


    def printMe(self):
        print "\nApartment in {0} street in {1} neighborhood".format(self.address,self.neighborhood)
        print "price: {}".format(self.price)
        print "size: {} sq, rooms: {}, floor: {}{}".format(self.size,self.rooms,self.floor,self.total_floors)
        print "details: {}".format(self.details)
        print "contact: {}[{}],{}".format(self.contact_name,self.contact_phone,self.agent)


