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
        postgreSQL_select_Query = """select message from order_upsseq where time > %s - INTERVAL '60 second'"""
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
            
        postgreSQL_update_Query = """update order_upsseq set time = %s where time > %s - INTERVAL '60 second'"""

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

def generate_ACommu():
    acommu = commu_pb2.ACommunicate()
    aloaded = acommu.aloaded.add()
    aloaded.packageid = 1; 
    aloaded.truckid = 2; 
    aloaded.seqnum = 3;
    return acommu

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
            print(status)
            break



    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return status == 'packed'

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
        for row in records:
            print("%s, %s" % (productmap[row[0]], row[1]))
            if productmap[row[0]] < row[1]:
                flag = False
                break
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
        return flag

    
def main():
    """
    acommu = generate_ACommu()
    insert_ACommunicate_to_DB(acommu, 3)
    insert_ACommunicate_to_DB(acommu, 4)
    delete_ACommunicate_to_DB([3])
    cmdlist = select_timeout_from_ACommunicate()
    for cmd in cmdlist:
        print(cmd)

    acommu = generate_ACommu()
    insert_ACommunicate_to_DB(acommu, 3)
    cmdlist = select_timeout_from_ACommunicate()
    for cmd in cmdlist:
        print(cmd)
    #result = pck_truck_arrived(1)
    #print(result)
    """
    productmap = check_warehouse()
    print(select_product(4, productmap))
if __name__ == '__main__':
    main()
