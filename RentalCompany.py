class Car:
    total_cars = 0  # Class variable: Total number of cars created

    def __init__(self, car_number, car_type='sedan'):
        self.car_number = car_number
        self.car_type = car_type
        self.customer_name = None
        Car.total_cars += 1

    def rent(self, customer_name):
        if self.customer_name is not None:
            raise Exception(f'Car {self.car_number} is already rented')
        self.customer_name = customer_name

    def return_car(self):
        if self.customer_name is None:
            raise Exception(f'Car {self.car_number} is not rented')
        self.customer_name = None

    def is_available(self):
        return self.customer_name is None

    def __str__(self):
        if self.customer_name is None:
            return f'Car {self.car_number} ({self.car_type}) is available'
        else:
            return f'Car {self.car_number} ({self.car_type}) is rented by {self.customer_name}'

    @classmethod
    def get_total_cars(cls):
        return cls.total_cars


class ElectricCar(Car):
    def __init__(self, car_number, battery_level=100):
        super().__init__(car_number, car_type='electric')
        self.battery_level = battery_level

    def charge(self, amount):
        self.battery_level = min(100, self.battery_level + amount)

    def consume_battery(self, amount):
        self.battery_level = max(0, self.battery_level - amount)

    def __str__(self):
        base_str = super().__str__()
        return f'{base_str}, Battery: {self.battery_level}%'


class RentalCompany:
    def __init__(self, cars_info):
        self.car_list = []
        for num, ctype in cars_info:
            if ctype == 'electric':
                self.car_list.append(ElectricCar(num))
            else:
                self.car_list.append(Car(num, ctype))

    def show_all_cars(self):
        for car in self.car_list:
            print(car)

    def rent_car(self, car_number, customer_name, preferred_type='sedan'):
        for car in self.car_list:
            if car.car_number == car_number and car.car_type == preferred_type:
                if car.is_available():
                    car.rent(customer_name)
                    return car.car_number
                else:
                    raise Exception(f'Car {car_number} is already rented')
        raise Exception(f'No available {preferred_type} car with number {car_number} for {customer_name}')

    def rent_auto(self, customer_name, preferred_type='sedan'):
        for car in self.car_list:
            if car.is_available() and car.car_type == preferred_type:
                car.rent(customer_name)
                return car.car_number
        raise Exception(f'No available {preferred_type} car for {customer_name}')

    def return_car_from(self, car_number):
        for car in self.car_list:
            if car.car_number == car_number:
                if not car.is_available():
                    if isinstance(car, ElectricCar):
                        # Consume 30% battery when the car is returned
                        car.consume_battery(30)
                    car.return_car()
                    return
                else:
                    raise Exception(f'Car {car_number} is already available')
        raise Exception(f'Invalid car number: {car_number}')


# --- Test Code ---
cars_info = [
    (1, 'sedan'),
    (2, 'electric'),
    (3, 'suv'),
    (4, 'electric')
]

company = RentalCompany(cars_info)

print("--- 全車両の状態 ---")
company.show_all_cars()

print("\n--- Aliceがsedanをレンタル ---")
company.rent_auto("Alice", preferred_type='sedan')

print("\n--- Aliceがすでに借りている車を再び借りようとする（エラー発生） ---")
try:
    company.rent_car(1, "Charlie", preferred_type='sedan')
except Exception as e:
    print("Error:", e)

print("\n--- Bobがelectricをレンタル ---")
company.rent_auto("Bob", preferred_type='electric')

print("\n--- 状態確認 ---")
company.show_all_cars()

print("\n--- Bobが車を返却（バッテリー30％消費） ---")
company.return_car_from(2)

print("\n--- 最終状態 ---")
company.show_all_cars()

print("\n--- 総車両数 ---")
print(Car.get_total_cars())
