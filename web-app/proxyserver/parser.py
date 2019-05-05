import amazon_pb2
import commu_pb2
import psycopg2

def get_name_from_DB(productid):
    # return "Apple"
    # connect to database
    try:
       connection = psycopg2.connect(user="postgres",
                                      password="passw0rd",
                                      host="67.159.88.129",
                                      port="5432",
                                      database="postgres")
       cursor = connection.cursor()
       postgreSQL_select_Query = "select productName from wareHouse where productId = " + productid
       cursor.execute(postgreSQL_select_Query)
       print("Selecting name from wareHouse table using cursor.fetchall")
       records = cursor.fetchall() 
       
       print("Print each row and it's columns values")
       name = str()
       for row in records:
           name = row[0]
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
    """
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            return name
    """

class WebRequestParser:
    def __init__(self, request):
        self.request = request
        self.ac = amazon_pb2.ACommands()     # generate a protocol buff
        self.uc = commu_pb2.UCommunicate()   # generate

    def isBuy(self):
        return request.whid == -100

    def getAPurchaseMore(self, seqnum):
        for aorderplaced in self.request.aorderplaced:
            buy = self.ac.buy.add()
            buy.whnum = aorderplaced.whid
            buy.seqnum = seqnum

            for product in aorderplaced.things:
                thing = buy.things.add()
                thing.id = int(product.name)
                thing.description = product.description
                thing.count = product.count



    def getAPack(self, seqnum):
        for aorderplaced in self.request.aorderplaced:
            topack = self.ac.topack.add()
            topack.whnum = aorderplaced.whid
            topack.shipid = aorderplaced.packageid
            topack.seqnum = seqnum

            for product in aorderplaced.things:
                thing = topack.things.add()
                thing.id = int(product.name)
                thing.description = product.description
                thing.count = product.count

    def getAOrderPlaced(self, seqnum):
        for aorderplaced in self.request.aorderplaced:
            for product in aorderplaced.things:
                productid = product.name
                product.name = get_name_from_DB(productid)
        self.uc = self.request

    def getACommands(self):
        return self.ac

    def getUCommunicate(self):
        return self.uc

class UPSParser:
    def __init__(self, request):
        self.request = request

    def associate_tid_pid(self):
        for uorder in self.request.uorderplaced:
            truckid = uorder.truckid
            packageid = uorder.packageid
            insert_into_DB_table(truckid, packageid)

    def send_APutOnTruck(self):
        acommand = amazon_pb2.ACommands()
        for uarrive in self.request.uarrived:
            infolist = search_for_truckid(uarrive.truckid)
            generate_APutOnTruck(infolist, acommand)

        return acommand

def insert_into_DB_table(truckid, packageid):
    pass


class WorldHandler:
    def __init__(self, request):
        self.request = request

    def handle_pack(self):
        for ready in self.request.ready:
            insert_package_status(ready.shipid, "packed")

    def handle_load(self):
        loadedlist = []
        for loaded in self.request.ready:
            loadedlist.append(loaded.shipid)

        if len(loaded):
            send_ALoadingFinished(loadedlist)

    def handle_package(self):
        for packagestatus in self.request:
            insert_package_status(packagestatus.shipid, packagestatus.status)