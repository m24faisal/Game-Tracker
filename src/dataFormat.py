from dataclasses import dataclass

@dataclass

class DataSnap:
    fps: float
    time: float
    date: str

    plyrName: str
    plyrLocation: list[float]
    plyrHealth: float
    # plyrInventory: list[int]
    plyrInventory: str
    # plyrStatus: list[int]
    plyrStatus: str
    plyrHunger: float
    plyrSat: float


def decrypt(data): # Takes dict as input, decrypts and returns the data class
    try:
        date = data.get('date')
        fps = float(data.get("fps"))
        time = data.get('time')
        plyrName = data.get('plyrName')
        plyrInventory = data.get('plyrInventory')
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


    
