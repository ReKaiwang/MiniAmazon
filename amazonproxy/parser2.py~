import amazon_pb2
import commu_pb2
import psycopg2
import protobuf_json
import datetime
import json

USER = "postgres"
PASSWORD = "passw0rd"
HOST = "152.3.53.20"
PORT = "5432"
DATABASE = "miniamazon"
buy_to_pckid = {}

class WebRequestParser:
    def __init__(self, request):
        self.request = request
        self.ac = amazon_pb2.ACommands()     # generate a protocol buff
        self.uc = commu_pb2.ACommunicate()   # generate
        self.deal_with_description()

    def deal_with_description(self):
        for aorderplaced in self.request.aorderplaced:
            for thing in aorderplaced.things:
                if len(thing.description) > 0:
                    thing.description = thing.description[0:10]

    def isBuy(self):
        for aorderplaced in self.request.aorderplaced:
            return aorderplaced.whid != -100

    def getAPurchaseMore(self, seqnum):
        seqlist = []
        for aorderplaced in self.request.aorderplaced:
            buy = self.ac.buy.add()
            buy.whnum = aorderplaced.whid
            buy.seqnum = aorderplaced.packageid * 10 + 4
            seqlist.append(buy.seqnum)

            for product in aorderplaced.things:
                thing = buy.things.add()
                thing.id = int(product.name)
                thing.description = product.description
                thing.count = product.count

        for seqnum in seqlist:
            insert_ACommands_to_DB(seqnum, self.ac)



    def getAPack(self, seqnum):
        acommand = amazon_pb2.ACommands()
        pckid = None
        for aorderplaced in self.request.aorderplaced:
            topack = acommand.topack.add()
            topack.whnum = aorderplaced.whid
            topack.shipid = aorderplaced.packageid
            pckid = topack.shipid
            topack.seqnum = topack.shipid * 10 + 5
            for product in aorderplaced.things:
                thing = topack.things.add()
                thing.id = int(product.name)
                thing.description = product.description
                thing.count = product.count

        insert_APack_to_DB(pckid, acommand)

    def getAOrderPlaced(self, seqnum):
        acommu = commu_pb2.ACommunicate()
        pckid = None
        for aorderplaced in self.request.aorderplaced:
            pckid = aorderplaced.packageid
            for product in aorderplaced.things:
                productid = product.name
                try:
                    product.name = get_name_from_DB(productid)
                except:
                    product.name = "Unknown"
            aorderplaced.seqnum = aorderplaced.packageid * 10 + 1

        acommu = self.request
        insert_AOrderPlaced_to_DB(pckid, acommu)
        # for seqnum in seqlist:
        #     insert_ACommunicate_to_DB(self.uc, seqnum)


    def getACommands(self):
        return self.ac

    def getACommunicate(self):
        return self.uc

class UPSParser:
    def __init__(self, request):
        self.request = request

    def generate_ack_response(self):
        acommu = commu_pb2.ACommunicate()
        for uorderplaced in self.request.uorderplaced:
            acommu.acks.append(uorderplaced.seqnum)
        for uarrived in self.request.uarrived:
            acommu.acks.append(uarrived.seqnum)
        for udelivered in self.request.udelivered:
            acommu.acks.append(udelivered.seqnum)

        return acommu

    def associate_tid_pid(self):
        for uorder in self.request.uorderplaced:
            truckid = uorder.truckid
            packageid = uorder.packageid
            insert_into_DB_table(truckid, packageid)

    def update_status(self):
        statustable = {}
        for uarrived in self.request.uarrived:
            pcklist = get_packageid_from_DB(uarrived.truckid, 'packing')
            for pckid in pcklist:
                statustable[pckid] = 'TruckArrived'

        for udelivered in self.request.udelivered:
            statustable[udelivered.packageid] = 'Delivered'
        update_status_DB(statustable)



    def get_APutOnTruck(self):
        acommand = amazon_pb2.ACommands()
        for uarrive in self.request.uarrived:
            pcklist = get_packageid_from_DB(uarrive.truckid, 'packed')
            generate_APutOnTruck(pcklist, uarrive.truckid, acommand)

        return acommand

    def delete_seq_in_DB(self):
        acklist = []
        for i in self.request.acks:
            acklist.append(i)
        delete_ACommunicate_to_DB(acklist)





class AResponseParser:
    def __init__(self, aresponse):
        self.aresponse = aresponse

    def generate_ack_response(self):
        seqlist = []
        for i in self.aresponse.arrived:
            seqlist.append(i.seqnum)
        for i in self.aresponse.ready:
            seqlist.append(i.seqnum)
        for i in self.aresponse.loaded:
            seqlist.append(i.seqnum)
        for i in self.aresponse.error:
            seqlist.append(i.seqnum)
        for i in self.aresponse.packagestatus:
            seqlist.append(i.seqnum)

        acommand = amazon_pb2.ACommands()
        for ack in seqlist:
            acommand.acks.append(ack)
        return acommand

    def add_num_in_warehouse(self):
        productcount = {}
        for arrived in self.aresponse.arrived:
            for thing in arrived.things:
                productcount[thing.id] = productcount.get(thing.id, 0) + thing.count
        update_count_in_DB(productcount)

    def delete_seq_in_DB(self):
        acklist = []
        for i in self.aresponse.acks:
            acklist.append(i)
        delete_ACommands_to_DB(acklist)

    def get_APutOnTruck(self):
        acommand = amazon_pb2.ACommands()
        for ready in self.aresponse.ready:
            if pck_truck_arrived(ready.shipid):
                truckid = get_truckid_from_DB(ready.shipid)
                generate_APutOnTruck([ready.shipid], truckid, acommand)

        return acommand

    def update_status(self):
        statustable = {}
        for ready in self.aresponse.ready:
            statustable[ready.shipid] = 'packed'
            # statuslist.append((ready.shipid, 'packed'))

        for loaded in self.aresponse.loaded:
            statustable[loaded.shipid] = 'loaded'
            # statuslist.append((loaded.shipid, 'loaded'))

        for packagestatus in self.aresponse.packagestatus:
            if packagestatus.shipid not in statustable:
                statustable[packagestatus.shipid] = packagestatus.status

        update_status_DB(statustable)

    def generate_ALoadingFinished(self):
        ac = commu_pb2.ACommunicate()

        loadlist = []
        for loaded in self.aresponse.loaded:
            pckid = loaded.shipid
            truckid = get_truckid_from_DB(pckid)
            loadlist.append((truckid, pckid))
        add_ALoadingFinished(loadlist, ac)

        return ac

    def get_package_status(self):
        statuslist = []
        for i in self.aresponse.packagestatus:
            statuslist.append([i.packageid, i.status])

        return statuslist






def get_packageid_from_DB(truckid, status):
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        postgreSQL_select_Query = """select order_truck.shipid
                                    from order_truck inner join order_orders on order_orders.shipid = order_truck.shipid
                                    where order_truck.truckid = %s and order_orders.status = %s"""
        pcklist = []
        print("Getting packageid using truckid from database")
        cursor.execute(postgreSQL_select_Query, (truckid, status))
        print("Selecting packageid from wareHouse table using cursor.fetchall")
        records = cursor.fetchall()

        print("Print each row and it's columns values")

        for row in records:
            pcklist.append(row[0])
        #postgreSQL_delete_Query = """delete from order_truck where truckid = %s"""
        #postgreSQL_delete_Query = 'delete from order_truck where "truckId" = ' + truckid
        #cursor.execute(postgreSQL_delete_Query)
        #connection.commit()



    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return pcklist


def update_status_DB(statustable):
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        print("update order_orders")
        print(statustable)
        for pckid, status in statustable.items():
            postgreSQL_update_Query = """update order_orders set status = %s where shipid = %s"""
            # postgreSQL_update_Query = "'" + status + "' where "shipId" = '" + str(pckid) + "'"
            print(postgreSQL_update_Query % (status, str(pckid)))
            cursor.execute(postgreSQL_update_Query, (status, str(pckid)))
            connection.commit()
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def add_ALoadingFinished(loadlist, ac):
    seqlist = []
    for truckid, pckid in loadlist:
        aloaded = ac.aloaded.add()
        aloaded.packageid = pckid
        aloaded.truckid = truckid
        aloaded.seqnum = pckid * 10 + 2
        seqlist.append(aloaded.seqnum)
    for seq in seqlist:
        insert_ACommunicate_to_DB(ac, seq)


def generate_APutOnTruck(pcklist, truckid, acommand):
    seqlist = []
    for pckid in pcklist:
        load = acommand.load.add()
        load.whnum = get_whnum_from_DB(pckid)
        load.truckid = truckid
        load.shipid = pckid
        load.seqnum = pckid*10 + 6
        seqlist.append(load.seqnum)
    for seq in seqlist:
        insert_ACommands_to_DB(seq, acommand)

def get_whnum_from_DB(pckid):
    return 1

def get_truckid_from_DB(pckid):
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        postgreSQL_select_Query = """select truckid from order_truck where shipid = %s"""
        #postgreSQL_select_Query = 'select "truckid" from order_truck where "shipid" = ' + str(pckid)
        print("Selecting truckid from wareHouse table using cursor.fetchall")
        print(postgreSQL_select_Query % (pckid, ))
        cursor.execute(postgreSQL_select_Query, (pckid, ))
        records = cursor.fetchall()

        print("Print each row and it's columns values")
        truckid = None
        for row in records:
            truckid = row[0]
            print("truckid is %s" % (truckid,))
        # postgreSQL_delete_Query = """delete from order_truck where truckid = %s"""
        #postgreSQL_delete_Query = 'delete from order_truck where "truckId" = ' + truckid
        # cursor.execute(postgreSQL_delete_Query, (truckid))
        #connection.commit()



    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return truckid

def insert_into_DB_table(truckid, packageid):
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        postgreSQL_insert_Query = """INSERT INTO order_truck (truckid, shipid) VALUES(%s, %s) ;"""
        print(postgreSQL_insert_Query % (truckid, packageid))
        cursor.execute(postgreSQL_insert_Query, (truckid, packageid))
        connection.commit()

        # postgreSQL_delete_Query = """delete from order_truck where truckId = %s"""
        # #postgreSQL_delete_Query = 'delete from order_truck where "truckId" = ' + truckid
        # cursor.execute(postgreSQL_delete_Query, (truckid,))
        #connection.commit()

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def get_name_from_DB(productid):
    # return "Apple"
    # connect to database
    try:
       connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
       cursor = connection.cursor()
       postgreSQL_select_Query = """select productname from order_warehouse where productid = %s"""
       print(postgreSQL_select_Query % (productid, ))
       cursor.execute(postgreSQL_select_Query, (productid, ))
       print("Selecting name from wareHouse table using cursor.fetchall")
       records = cursor.fetchall()

       print("Print each row and it's columns values")
       name = str()
       for row in records:
           name = row[0]
           break

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return name


def pck_truck_arrived(pckid):
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        postgreSQL_select_Query = """select status from order_orders where shipid = %s"""
        #postgreSQL_select_Query = 'select "truckid" from order_truck where "shipid" = ' + str(pckid)
        print(postgreSQL_select_Query % (pckid,))
        cursor.execute(postgreSQL_select_Query, (pckid,))
        print("Selecting status from wareHouse table using cursor.fetchall")
        records = cursor.fetchall()

        print("Print each row and it's columns values")
        status = 'InWareHouse'
        for row in records:
            status = row[0]
            break



    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return status == 'TruckArrived'

def insert_APack_to_DB(pckid, acommand):
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        jsonobj = protobuf_json.pb2json(acommand)

        print(jsonobj)
        postgreSQL_insert_Query = """INSERT INTO order_topack (packageid, message) VALUES(%s, %s) ;"""
        records = (pckid, json.dumps(jsonobj))
        print(postgreSQL_insert_Query % records)
        cursor.execute(postgreSQL_insert_Query, records)
        connection.commit()

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def insert_AOrderPlaced_to_DB(pckid, acommu):
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        jsonobj = protobuf_json.pb2json(acommu)

        print(jsonobj)
        postgreSQL_insert_Query = """INSERT INTO order_placed (packageid, message) VALUES(%s, %s) ;"""
        records = (pckid, json.dumps(jsonobj))
        print(postgreSQL_insert_Query % records)
        cursor.execute(postgreSQL_insert_Query, records)
        connection.commit()

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def insert_ACommands_to_DB(seqnum, acommu):
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        jsonobj = protobuf_json.pb2json(acommu)

        print(type(jsonobj))
        postgreSQL_insert_Query = """INSERT INTO order_worldseq (seqnum, message, time) VALUES(%s, %s, %s) ;"""
        records = (seqnum, json.dumps(jsonobj), datetime.datetime.now())
        print(postgreSQL_insert_Query % records)
        cursor.execute(postgreSQL_insert_Query, records)
        connection.commit()

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def delete_ACommands_to_DB(acklist):
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        for ack in acklist:
            postgreSQL_delete_Query = """delete from order_worldseq where seqnum = %s"""
            try:
                cursor.execute(postgreSQL_delete_Query, (ack,))
                connection.commit()
            except:
                continue

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def select_timeout_from_ACommands():
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        # SELECT * FROM mytable WHERE "date" >= NOW() - INTERVAL '1 minutes';
        #postgreSQL_select_Query = """select message from order_upsseq where time >  (current_timestamp - make_interval(secs := %s))"""
        #intervalInSecs = 300;
        #print(postgreSQL_select_Query % intervalInSecs)
        #cursor.execute(postgreSQL_select_Query, [intervalInSecs])
        postgreSQL_select_Query = """select message from order_worldseq where time < %s - INTERVAL '30 second'"""
        print(postgreSQL_select_Query)
        dt = datetime.datetime.now()
        cursor.execute(postgreSQL_select_Query, [dt])


        print("Selecting message from wareHouse table using cursor.fetchall")
        records = cursor.fetchall()

        print("Print each row and it's columns values")
        cmdlist = []
        for row in records:
            jsonobj = row[0]
            cmd = protobuf_json.json2pb(amazon_pb2.ACommands(), jsonobj)
            cmdlist.append(cmd)

        postgreSQL_update_Query = """update order_worldseq set time = %s where time < %s - INTERVAL '30 second'"""

        #postgreSQL_delete_Query = 'delete from order_truck where "truckId" = ' + truckid
        cursor.execute(postgreSQL_update_Query, (datetime.datetime.now(), datetime.datetime.now()))
        connection.commit()


    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return cmdlist



def insert_ACommunicate_to_DB(acommu, seqnum):
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        jsonobj = protobuf_json.pb2json(acommu)

        print(type(jsonobj))
        postgreSQL_insert_Query = """INSERT INTO order_upsseq (seqnum, message, time) VALUES(%s, %s, %s) ;"""
        records = (seqnum, json.dumps(jsonobj), datetime.datetime.now())
        print(postgreSQL_insert_Query % records)
        cursor.execute(postgreSQL_insert_Query, records)
        connection.commit()

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def select_timeout_from_ACommunicate():
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        # SELECT * FROM mytable WHERE "date" >= NOW() - INTERVAL '5 minutes';
        #postgreSQL_select_Query = """select message from order_upsseq where time >  (current_timestamp - make_interval(secs := %s))"""
        #intervalInSecs = 300;
        #print(postgreSQL_select_Query % intervalInSecs)
        #cursor.execute(postgreSQL_select_Query, [intervalInSecs])
        postgreSQL_select_Query = """select message from order_upsseq where time < %s - INTERVAL '30 second'"""
        print(postgreSQL_select_Query)
        dt = datetime.datetime.now()
        cursor.execute(postgreSQL_select_Query, [dt])


        print("Selecting message from wareHouse table using cursor.fetchall")
        records = cursor.fetchall()

        print("Print each row and it's columns values")
        cmdlist = []
        for row in records:
            jsonobj = row[0]
            cmd = protobuf_json.json2pb(commu_pb2.ACommunicate(), jsonobj)
            cmdlist.append(cmd)

        postgreSQL_update_Query = """update order_upsseq set time = %s where time < %s - INTERVAL '30 second'"""

        #postgreSQL_delete_Query = 'delete from order_truck where "truckId" = ' + truckid
        cursor.execute(postgreSQL_update_Query, (datetime.datetime.now(), datetime.datetime.now()))
        connection.commit()



    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return cmdlist

def delete_ACommunicate_to_DB(acklist):
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        for ack in acklist:
            postgreSQL_delete_Query = """delete from order_upsseq where seqnum = %s"""
            try:
                cursor.execute(postgreSQL_delete_Query, (ack,))
                connection.commit()
            except:
                continue

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def find_ToPack(shipid):
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        # SELECT * FROM mytable WHERE "date" >= NOW() - INTERVAL '5 minutes';
        #postgreSQL_select_Query = """select message from order_upsseq where time >  (current_timestamp - make_interval(secs := %s))"""
        #intervalInSecs = 300;
        #print(postgreSQL_select_Query % intervalInSecs)
        #cursor.execute(postgreSQL_select_Query, [intervalInSecs])
        postgreSQL_select_Query = """select message from order_topack where packageid = %s"""
        print(postgreSQL_select_Query % (shipid,))

        cursor.execute(postgreSQL_select_Query, (shipid, ))


        print("Selecting message from order_topack table using cursor.fetchall")
        records = cursor.fetchall()

        print("Print each row and it's columns values")
        cmd = None
        for row in records:
            jsonobj = row[0]
            cmd = protobuf_json.json2pb(amazon_pb2.ACommands(), jsonobj)
            break
        if cmd:
            for topack in cmd.topack:
                insert_ACommands_to_DB(topack.seqnum, cmd)

        postgreSQL_delete_Query = """delete from order_topack where packageid = %s"""


        #postgreSQL_delete_Query = 'delete from order_truck where "truckId" = ' + truckid
        cursor.execute(postgreSQL_delete_Query, (shipid, ))
        connection.commit()



    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return cmd

def find_AOrderPlaced(shipid):
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        # SELECT * FROM mytable WHERE "date" >= NOW() - INTERVAL '5 minutes';
        #postgreSQL_select_Query = """select message from order_upsseq where time >  (current_timestamp - make_interval(secs := %s))"""
        #intervalInSecs = 300;
        #print(postgreSQL_select_Query % intervalInSecs)
        #cursor.execute(postgreSQL_select_Query, [intervalInSecs])
        postgreSQL_select_Query = """select message from order_placed where packageid = %s"""
        print(postgreSQL_select_Query % (shipid,))

        cursor.execute(postgreSQL_select_Query, (shipid, ))


        print("Selecting message from order_topack table using cursor.fetchall")
        records = cursor.fetchall()

        print("Print each row and it's columns values")
        cmd = None
        for row in records:
            jsonobj = row[0]
            cmd = protobuf_json.json2pb(commu_pb2.ACommunicate(), jsonobj)
            break
        if cmd:
            for aorderplaced in cmd.aorderplaced:
                insert_ACommunicate_to_DB(cmd, aorderplaced.seqnum)
                # insert_A_to_DB(aorderplaced.seqnum, cmd)

        postgreSQL_delete_Query = """delete from order_placed where packageid = %s"""


        #postgreSQL_delete_Query = 'delete from order_truck where "truckId" = ' + truckid
        cursor.execute(postgreSQL_delete_Query, (shipid, ))
        connection.commit()



    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return cmd


def generate_Commands():
    pckid = get_packageid()
    if pckid:
        acommand = find_ToPack(pckid)
        acommu = find_AOrderPlaced(pckid)
        if not acommand:
            print("did not add related APack")
        if not acommu:
            print("did not add related AOrderPlaced")

        return (acommand, acommu)

    return (None, None)

def get_packageid():
    pcklist = get_inWarehouse_packageid()
    productmap = check_warehouse()
    for pckid in pcklist:
        if select_product(pckid, productmap):
            return pckid
    return None

def get_inWarehouse_packageid():
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        pcklist = []
        postgreSQL_select_Query = """select shipid from order_orders where status = %s"""
        cursor.execute(postgreSQL_select_Query, ('InWareHouse', ))
        records = cursor.fetchall()
        for row in records:
            pcklist.append(row[0])

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return pcklist


def check_warehouse():
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        productmap = {}
        postgreSQL_select_Query = """select productid, count from order_warehouse"""
        cursor.execute(postgreSQL_select_Query)
        records = cursor.fetchall()
        for row in records:
            productmap[row[0]] = row[1]

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return productmap

def select_product(shipid, productmap):
    try:
        flag = False
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()

        postgreSQL_select_Query = """select productid, count from cart_carts where ship_id = %s"""

        #postgreSQL_select_Query = """select order_truck.shipid
        #                            from order_truck inner join order_orders on order_orders.shipid = order_truck.shipid
        #                            where order_truck.truckid = %s and order_orders.status = %s"""


        cursor.execute(postgreSQL_select_Query, (shipid, ))

        records = cursor.fetchall()

        print("Print each row and it's columns values")
        i = 0
        flag = True
        productcount = {}
        for row in records:
            productcount[row[0]] = row[1]
            print("%s, %s" % (productmap[row[0]], row[1]))
            if productmap[row[0]] < row[1]:
                flag = False
                break
        #postgreSQL_delete_Query = """delete from order_truck where truckid = %s"""
        #postgreSQL_delete_Query = 'delete from order_truck where "truckId" = ' + truckid
        #cursor.execute(postgreSQL_delete_Query)
        #connection.commit()
        if flag:
            for productid, count in productcount.items():
                postgreSQL_update_Query = """update order_warehouse set count = count - %s where productid = %s"""
                print(postgreSQL_update_Query % (count, productid))
                cursor.execute(postgreSQL_update_Query, (count, productid))
                connection.commit()
            statustable = {}
            statustable[shipid] = 'packing'
            update_status_DB(statustable)


    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return flag


def update_count_in_DB(productcount):
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        print("update order_warehouse")
        print(productcount)
        for pckid, count in productcount.items():
            postgreSQL_update_Query = """update order_warehouse set count = count + %s where productid = %s"""
            # postgreSQL_update_Query = "'" + status + "' where "shipId" = '" + str(pckid) + "'"
            print(postgreSQL_update_Query % (count, pckid))
            cursor.execute(postgreSQL_update_Query, (count, pckid))
            connection.commit()
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
