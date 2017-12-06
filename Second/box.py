read_data = []

class box:
    _items = 0
    _value = 0
    _volume = 0
    _weight = 0
    new = False
    health = 1 #штрафы за старость

    def __init__(self, items:int):
        self.setItems(items)

    def getItems(self)->int:
        return self._items

    def getItemList(self)->list:
        return [x+1 for x in range(0,30) if self.containsItem(x)]

    def setItems(self, items:int):
        self._items = items
        self.recalc()

    def inverseItem(self, index: int):
        self._items ^= 1 << index

    def containsItem(self,index:int) -> bool:
        return (self._items >> index) & 1 == 1

    def recalc(self):
        self._value = 0
        self._volume = 0
        self._weight = 0
        for i in range(0,30):
            if self.containsItem(i):
                self._value += read_data[i]["value"]
                self._volume += read_data[i]["volume"]
                self._weight += read_data[i]["weight"]

    def getVal(self) -> int:
        return self._value*self.health
    def getValPure(self) -> int:
        return self._value
    def getVlm(self) -> float:
        return self._volume
    def getWei(self) -> int:
        return self._weight