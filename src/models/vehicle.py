from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, vehicle_id, brand, model, year, license_plate, status, daily_rate):
        self._vehicle_id = vehicle_id
        self._brand = brand
        self._model = model
        self._year = year
        self._license_plate = license_plate
        self._status = status
        self._daily_rate = daily_rate

    @property
    def vehicle_id(self):
        return self._vehicle_id

    @property
    def description(self):
        return f"{self._year} {self._brand} {self._model}"

    @property
    def status(self):
        return self._status

    @property
    def daily_rate(self):
        return self._daily_rate

    @abstractmethod
    def calculate_rental_cost(self, days):
        pass

class Car(Vehicle):
    def calculate_rental_cost(self, days):
        return self._daily_rate * days

class Truck(Vehicle):
    def calculate_rental_cost(self, days):
        # Trucks might have a base fee + daily rate
        return (self._daily_rate * days) + 500 

class SUV(Vehicle):
    def calculate_rental_cost(self, days):
        return self._daily_rate * days

class Van(Vehicle):
    def calculate_rental_cost(self, days):
        return self._daily_rate * days

class Motorcycle(Vehicle):
    def calculate_rental_cost(self, days):
        return self._daily_rate * days
