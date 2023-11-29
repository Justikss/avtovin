class CarCharacteristic:
    def __init__(self, name, options):
        self.name = name
        self.options = options  # Словарь опций

class CarModel:
    def __init__(self, name):
        self.name = name
        self.characteristics = []  # Список объектов CarCharacteristic

    def add_characteristic(self, characteristic):
        if isinstance(characteristic, list):
            for one_characteristic in characteristic:
                self.characteristics.append(one_characteristic)
        else:
            self.characteristics.append(characteristic)

class CarBrand:
    def __init__(self, name):
        self.name = name
        self.models = []  # Список объектов CarModel

    def add_model(self, model):
        if isinstance(model, list):
            for one_model in model:
                self.models.append(one_model)
        else:
            self.models.append(model)

class CarComplectation:
    def __init__(self, name):
        self.name = name
        self.brands = []  # Список объектов CarBrand

    def add_brand(self, brand):
        if isinstance(brand, list):
            for one_brand in brand:
                self.brands.append(one_brand)
        else:
            self.brands.append(brand)


characteristics = list()
models = list()
brands = list()
complectations = list()

async def create_characteristic(name, options):
    global characteristics
    new = CarCharacteristic

    characteristics.append(new)

async def model(name, characteristic=None):
    global models

    exists_model = [model for model in models if model.name == name]
    if exists_model and characteristic:
        exists_model[0].add_characteristic(characteristic)
    new = CarModel(name)

    if characteristic:
        new.add_characteristic(characteristic)

    models.append(new)

async def brand(name, model=None):
    global brands

    exists_brand = [brand for brand in brands if brand.name == name]
    if exists_brand and model:
        exists_brand[0].add_model(model)
    new = CarBrand(name)

    if model:
        new.add_model(model)

    brands.append(new)

async def complectation(name, brand=None):
    global complectations

    exists_complectation = [complectation for complectation in complectations if complectation.name == name]
    if exists_complectation and brand:
        exists_complectation[0].add_brand(brand)
    new = CarComplectation(name)

    if brand:
        new.add_brand(brand)

    complectations.append(new)

states = [CarCharacteristic('State', 'Used'), CarCharacteristic('State', 'New')]

engine_types = [CarCharacteristic('Engine type', 'Electro'), CarCharacteristic('Engine type', 'Hybrid'), CarCharacteristic('Engine type', 'DWS')]

brands = {'BYD': CarBrand('BYD'), 'Leapmotor': CarBrand('Leapmotor'), 'Li Xiang': CarBrand('Li Xiang'), 'Сhevrolet': CarBrand('Сhevrolet')}

models = {'C11': CarModel('C11'), 'SONG PLUS CHAMPION': CarModel('SONG PLUS CHAMPION'), 'CHAZOR': CarModel('CHAZOR'), 'Gentra': CarModel('Gentra'), 'Nexia 3': CarModel('Nexia 3')}

complectations = {'2': CarComplectation('2'), '3': CarComplectation('3'), 'L9 Pro': CarComplectation('L9 Pro'), 'L9 Max': CarComplectation('L9 Max')}
complects = [CarComplectation('Dual Motor 4WD 580 Km'), CarComplectation('Deluxe Edition 500 km (1)'), CarComplectation, CarComplectation('FLAGSHIP PLUS 605 km')]

[complect for complect in complects if complect.name == 'Dual Motor 4WD 580 Km'][0].add_brand(brands)

brands['BYD'].add_model([models['CHAZOR'], models['SONG PLUS CHAMPION']])
brands['Leapmotor'].add_model([models['C11']])
brands['Li Xiang'].add_model([models['L9'], models['L7']])
brands['Сhevrolet'].add_model([models['Gentra'], models['Nexia 3']])
