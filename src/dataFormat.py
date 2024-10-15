from dataclasses import dataclass

@dataclass

class DataSnap:
    fps: float
    time: float
    date: str

    plyrName: str
    plyrLocation: list[float]
    plyrHealth: int
    plyrInventory: list[int]
    plyrStatus: list[int]
    plyrHunger: int
    plyrSat: int


def decrypt(data): # Takes dict as input, decrypts and returns the data class
    try:
        fps = int(data.get("fps"))
        time = data.get('time')
        plyrName = data.get('plyrName')
        plyrInventory = data.get('plyrInventory')
        plyrStatus = data.get('plyrStatus')
        plyrLocation = eval(data.get('plyrLocation'))
        plyrHealth = int(data.get('plyrHealth'))
        plyrHunger = int(data.get('plyrHunger'))
        plyrSat = int(data.get('plyrSat'))


        return DataSnap(
            fps = fps,
            time = time,
        )
    except Exception as e:
        print(e)
        print('decrypt failed with data: ', data)
        return None


    
