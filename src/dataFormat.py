from dataclasses import dataclass
import csv

@dataclass 
class Item:
    name : str
    count : int
    meta : str

@dataclass
class DataSnap:
    fps: float
    time: float
    date: str

    plyrName: str
    plyrLocation: list[float]
    plyrHealth: float
    # plyrInventory: list[int]
    plyrInventory: list[Item]
    plyrArmor: str
    plyrOffhand: str
    # plyrStatus: list[int]
    plyrStatus: str
    plyrHunger: float
    plyrSat: float

def cleanSplit( source: str, token: str):
    return [s.strip() for s in source.split(token) if s.strip() != '']


def decryptInv(plyrInventory : str):
    out = []
    plyrInventory = cleanSplit(plyrInventory, ";")
    for pI in plyrInventory:
        itemName, itemCount = list(i.split(":")[1] for i in pI.split(","))
        out.append(Item(name = itemName, count = int(itemCount.strip()), meta = ""))
    return out

def decrypt(data): # Takes dict as input, decrypts and returns the data class
    try:
        date = data.get('date')
        fps = float(data.get("fps"))
        time = data.get('time')
        plyrName = data.get('plyrName')
        plyrInventory = decryptInv(data.get('plyrInventory'))
        plyrArmor = data.get('plyrArmor')
        plyrOffhand = data.get('plyrOffhand')
        plyrStatus = data.get('plyrStatus')
        plyrLocation = eval(data.get('plyrLocation'))
        plyrHealth = float(data.get('plyrHealth'))
        plyrHunger = float(data.get('plyrHunger'))
        plyrSat = float(data.get('plyrSat'))
        
        

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
            plyrSat = plyrSat
        )
    except Exception as e:
        print(e)
        print('decrypt failed with data: ', data)
        return None
def save_to_csv(data, filename):
    data_dict = {"date": data.date, "fps": data.fps, "time": data.time, "plyrName": data.plyrName,
        "plyrInventory": data.plyrInventory, "plyrArmor": data.plyrArmor, "plyrOffhand": data.plyrOffhand,
        "plyrStatus": data.plyrStatus, "plyrLocation": data.plyrLocation, "plyrHealth": data.plyrHealth,
        "plyrHunger": data.plyrHunger, "plyrSat": data.plyrSat}
    # Open a CSV file to write the data
    with open(filename, mode='a', newline="") as file:
        writer = csv.DictWriter(file,fieldnames=data_dict.keys())

        writer.writeheader()

        writer.writerow(data_dict)

def load_from_csv(filename):
    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        # Since it's a single row, convert the first row into a dictionary
        data = next(reader)
        # The code noted below may or may not be needed
        data = decrypt(data)
        return data



""" if u run this file standalone it will simply test some stuff"""
if __name__ == "__main__":
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
