class Car:
    
    def __init__(self, horse_power, make,mileage) -> None:
        self.engine = horse_power
        self.make = make
        self.mileage = mileage
    
    def PresentCar(self):
        return f"This {self.make} has {self.engine} and is currently at {self.mileage}"
    
    
    
class EV(Car):
    def __init__(self, batterty_level,**kwargs) -> None:
        super().__init__(**kwargs)
        self.battery = batterty_level
        
    def PresentCar(self):
        return super().PresentCar(), f"And has {self.battery}%"
    
    
car1 = Car(212, 'Ford', '13232')
ev1 = EV(89,horse_power = 154, make='Honda',mileage=32124)

car1.PresentCar()
ev1.PresentCar()
