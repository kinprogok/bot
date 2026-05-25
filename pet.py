import time
import random



class pet:
    def __init__(self):
        name = ["Шарик", "Бобик", "Жорик", "Воитель", "Бездельник"]
        surname = ["Шустрый ","Ловкий ","Сильный ", "Корявый ", "Горбатый "]
        self.name = random.choice(surname)+random.choice(name)
        self.level = 1
        self.ex = 0
        self.max_ex = 200
        self.power = 20
        self.hp = 100
        self.max_hp = self.hp
        self.energy = 100
        self.max_energy = 100
        self.last_update = time.time()

    def to_dict(self):
        return{
            "name":self.name,
            "level":self.level,
            "ex":self.ex,
            "max_ex":self.max_ex,
            "power":self.power,
            "hp":self.hp,
            "max_hp":self.max_hp,
            "energy":self.energy,
            "max_energy":self.max_energy,
            "last_update": self.last_update

            }

    @classmethod
    def from_dict(cls, data):
        new_pet = cls()
        new_pet.name = data["name"]
        new_pet.level = data["level"]
        new_pet.ex = data["ex"]
        new_pet.max_ex = data["max_ex"]
        new_pet.power = data["power"]
        new_pet.hp = data["hp"]
        new_pet.max_hp = data["max_hp"]
        new_pet.energy = data["energy"]
        new_pet.max_energy = data["max_energy"]
        new_pet.last_update = data["last_update"]
        return new_pet



    def upgrade(self):
        self.update_energy()
        self.ex +=20
        self.energy -= 10
        self.last_update = time.time()



        if self.ex >=self.max_ex:
            self.ex = 0
            self.level +=1
            self.power +=5
            self.max_hp +=20


    def heal(self):
        self.update_energy()
        self.hp +=20
        self.energy -= 15
        self.last_update = time.time()

        if self.hp >=self.max_hp:
            self.hp = self.max_hp

    def update_energy(self):
        now = time.time()
        time_past = now - self.last_update
        energy_add = int(time_past//10)
        if energy_add > 0:
                self.energy +=energy_add


                if energy_add > self.max_energy:
                    self.energy = self.max_energy

                self.last_update = time.time()

