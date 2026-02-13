class Vehicle:
    def __init__(self, vehicle_id, brand, model, year, license_plate, status, daily_rate):
        self._vehicle_id = vehicle_id
        self._brand = brand
        self._model = model
        self._year = year
        self._license_plate = license_plate
        self._status = status
        self._daily_rate = daily_rate

    def get_vehicle_id(self):
        return self._vehicle_id

    def get_brand(self):
        return self._brand

    def set_brand(self, brand):
        self._brand = brand

    def get_model(self):
        return self._model

    def set_model(self, model):
        self._model = model

    def get_year(self):
        return self._year

    def set_year(self, year):
        self._year = year

    def get_license_plate(self):
        return self._license_plate

    def set_license_plate(self, license_plate):
        self._license_plate = license_plate

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def get_daily_rate(self):
        return self._daily_rate

    def set_daily_rate(self, daily_rate):
        self._daily_rate = daily_rate

    def get_description(self):
        return str(self._year) + " " + str(self._brand) + " " + str(self._model)

    def calculate_rental_cost(self, days):
        raise NotImplementedError("Child class must implement calculate_rental_cost")

    vehicle_id = property(get_vehicle_id)
    description = property(get_description)
    status = property(get_status, set_status)
    daily_rate = property(get_daily_rate, set_daily_rate)

class Car(Vehicle):
    def calculate_rental_cost(self, days):
        return self._daily_rate * days

class Truck(Vehicle):
    def calculate_rental_cost(self, days):
        return (self._daily_rate * days) 

class SUV(Vehicle):
    def calculate_rental_cost(self, days):
        return self._daily_rate * days

class Van(Vehicle):
    def calculate_rental_cost(self, days):
        return self._daily_rate * days

class Motorcycle(Vehicle):
    def calculate_rental_cost(self, days):
        return self._daily_rate * days
