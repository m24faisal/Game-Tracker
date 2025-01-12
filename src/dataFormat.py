from dataclasses import dataclass, asdict
import csv
from dbManage import Database as db
import os

@dataclass 
class Item:
    name : str
    count : int
    meta : str

@dataclass
class Effect:
    name : str
    type : str
    duration : float
    amplifierLevel : int


@dataclass
class DataSnap:
    fps: float
    time: float
    date: str

    plyrName: str
    plyrLocation: list[float]
    plyrHealth: float
    plyrInventory: list[Item]
    plyrArmor: str
    plyrOffhand: str
    plyrStatus: list[Effect]
    plyrHunger: float
    plyrSat: float
    plyrView: list[float]
    plyrFacing: str
    plyrSelectedSlot: int
    plyrSelectedItem: str
    plyrRideState: bool
    plyrRideVehicle: str
    plyrMomentum: float 

def string_to_bool(value):
    truthy_values = {"true", "1", "yes", "on"}
    falsy_values = {"false", "0", "no", "off"}
    
    if not isinstance(value, str):
        value = str(value)

    # Normalize the input
    value = value.strip().lower()
    
    if value in truthy_values:
        return True
    elif value in falsy_values:
        return False
    else:
        raise ValueError(f"Cannot convert '{value}' to a boolean")
def cleanSplit( source: str, token: str):
    return [s.strip() for s in source.split(token) if s.strip() != '']

"""
def pairwiseGenerator(listObj):
    it = iter(listObj)
    one = next(it, None)  # Get the first element
    two = next(it, None)  # Get the first element
    while one != None and two != None:
        yield one, two
        one = next(it, None)  # Get the first element
        two = next(it, None)  # Get the first element
"""

def decryptInv(plyrInventory : str):
    out = []
    plyrInventory = cleanSplit(plyrInventory, ";")
    for pI in plyrInventory:
        itemName, itemCount = list(i.split(":")[1] for i in pI.split(","))
        out.append(Item(name = itemName, count = int(itemCount.strip()), meta = ""))
    return out

def decryptStatus(status : str):
    out = []
    status = status.strip()
    #print("status", status)
    if(status == 'None'):
        return out
    else:
        for stat in cleanSplit(status, ";"):
            stat = stat.strip()
            fragmentVals = []
            for fragment in cleanSplit(stat, ','):
                fragmentVals.append(cleanSplit(fragment, ":")[1])

            out.append(
                Effect( name = fragmentVals[0], 
                        type = fragmentVals[1], 
                        duration= float(fragmentVals[2]),
                        amplifierLevel= int(fragmentVals[3])
                )
            )
    return out

def decrypt(data) -> DataSnap: # Takes dict as input, decrypts and returns the data class
    try:
        date = data.get('date')
        fps = float(data.get("fps"))
        time = data.get('time')
        plyrName = data.get('plyrName')
        plyrInventory = decryptInv(data.get('plyrInventory'))
        plyrArmor = data.get('plyrArmor')
        plyrOffhand = data.get('plyrOffhand')
        plyrStatus = decryptStatus(data.get('plyrStatus'))
        plyrLocation = eval(data.get('plyrLocation'))
        plyrHealth = float(data.get('plyrHealth'))
        plyrHunger = float(data.get('plyrHunger'))
        plyrSat = float(data.get('plyrSat'))
        plyrView = eval(data.get('plyrView'))
        plyrFacing = data.get('plyrFacing'),
        plyrSelectedSlot = int(data.get('plyrSelectedSlot')),
        plyrSelectedItem = data.get('plyrSelectedItem'),
        plyrRideState = string_to_bool(data.get('plyrRideState')),
        plyrRideVehicle = data.get('plyrRideVehicle'),
        plyrMomentum = float(data.get('plyrMomentum'))

        return DataSnap(
            date = date,
            fps = fps,
            time = time,
            plyrName = plyrName,
            plyrInventory = plyrInventory,
            plyrArmor = plyrArmor,
            plyrOffhand = plyrOffhand,
            plyrStatus = plyrStatus,
            plyrLocation = plyrLocation,
            plyrHealth = plyrHealth,
            plyrHunger = plyrHunger,
            plyrSat = plyrSat,
            plyrView = plyrView,
            plyrFacing = plyrFacing,
            plyrSelectedSlot = plyrSelectedSlot,
            plyrSelectedItem = plyrSelectedItem,
            plyrRideState = plyrRideState,
            plyrRideVehicle = plyrRideVehicle,
            plyrMomentum = plyrMomentum
        )
    except Exception as e:
        print(e)
        
        print('decrypt failed with data: ')
        return None
def save_to_csv(data, filename):
    data_dict = asdict(data)
    # Open a CSV file to write the data
    with open(filename, mode='a', newline="") as file:
        writer = csv.DictWriter(file,fieldnames=data_dict.keys())

        if os.path.exists(filename) and os.stat(filename).st_size == 0:
            writer.writeheader()

        writer.writerow(data_dict)

def load_from_csv(filename):
    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        # Convert each row in the csv file to a dictionary which is then added to a list of dictionaries
        #print(dataDicts)
        outputData = []
        # The code noted below may or may not be needed
        for dataDict in reader:
            #datadict to datastruct
            outputData.append(DataSnap(**dataDict)) # named tuple from dictionary and then used as constructor for datastruct. fingers crossed
        return outputData

def save_to_database(dataObjects,table_name):
    if(isinstance(dataObjects, DataSnap)):
        dataObjects = [dataObjects]
    elif(isinstance(dataObjects, list)):
        pass
    else:
        return # not valid

    for dataObj in dataObjects:
        #print(data)
        data_dict = asdict(dataObj)
        db.createTable(table_name, data_dict)
        db.insertData(table_name, data_dict)


def test1():
    """test stuff"""
    print("testing data format decrypt")
    print("\n\neg. plyrInv...:")
    nameCount = {
        "bub" : "123",
        "nub1" : "230",
        "moob" : "45",
        "rob" : "93"
    }
    pI = ''
    for idx, i in enumerate(nameCount.items()):
        pI += f"Main Inventory {idx}: {i[0]}, Count: {i[1]}; "
    print(pI, "\n => \n", decryptInv(pI))

def test2():
    data = load_from_csv("../saves/playerData_01_11_2025_22_23_01.csv")
    print("data", data[0])
    save_to_database(data, "DATA")
def test3():
    q = "SELECT tablename, schemaname FROM pg_catalog.pg_tables WHERE tablename = 'data';"
    db.custom_command(q)
""" if u run this file standalone it will simply test some stuff"""
if __name__ == "__main__":
    test2()
    test3()