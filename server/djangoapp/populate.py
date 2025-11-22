from .models import (  # Ensure CarModel is imported if needed, usually only CarMake and CarModel suffice
    CarMake, CarModel)


def initiate():
    """
    Populates the CarMake and CarModel tables with initial data.
    This function is called by get_cars() if the database is empty.
    """
    # Define CarMake data
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]

    # Create CarMake instances and store them for linking
    car_make_instances = []
    for data in car_make_data:
        # Use get_or_create to prevent errors if the function is run multiple times
        make, created = CarMake.objects.get_or_create(
            name=data["name"], defaults={"description": data["description"]}
        )
        car_make_instances.append(make)

    # Define CarModel data (linking via the created CarMake instances)
    car_model_data = [
        # NISSAN (Index 0)
        {
            "name": "Pathfinder",
            "type": "SUV",
            "year": 2023,
            "car_make": car_make_instances[0],
            "dealer_id": 1,
        },
        {
            "name": "Qashqai",
            "type": "SUV",
            "year": 2023,
            "car_make": car_make_instances[0],
            "dealer_id": 2,
        },
        {
            "name": "XTRAIL",
            "type": "SUV",
            "year": 2023,
            "car_make": car_make_instances[0],
            "dealer_id": 3,
        },
        # Mercedes (Index 1)
        {
            "name": "A-Class",
            "type": "SUV",
            "year": 2023,
            "car_make": car_make_instances[1],
            "dealer_id": 1,
        },
        {
            "name": "C-Class",
            "type": "SUV",
            "year": 2023,
            "car_make": car_make_instances[1],
            "dealer_id": 4,
        },
        {
            "name": "E-Class",
            "type": "SUV",
            "year": 2023,
            "car_make": car_make_instances[1],
            "dealer_id": 5,
        },
        # Audi (Index 2)
        {
            "name": "A4",
            "type": "SEDAN",
            "year": 2023,
            "car_make": car_make_instances[2],
            "dealer_id": 2,
        },
        {
            "name": "A5",
            "type": "SEDAN",
            "year": 2023,
            "car_make": car_make_instances[2],
            "dealer_id": 6,
        },
        {
            "name": "A6",
            "type": "SEDAN",
            "year": 2023,
            "car_make": car_make_instances[2],
            "dealer_id": 7,
        },
        # Kia (Index 3)
        {
            "name": "Sorrento",
            "type": "SUV",
            "year": 2023,
            "car_make": car_make_instances[3],
            "dealer_id": 3,
        },
        {
            "name": "Carnival",
            "type": "WAGON",
            "year": 2023,
            "car_make": car_make_instances[3],
            "dealer_id": 8,
        },
        {
            "name": "Cerato",
            "type": "SEDAN",
            "year": 2023,
            "car_make": car_make_instances[3],
            "dealer_id": 9,
        },
        # Toyota (Index 4)
        {
            "name": "Corolla",
            "type": "SEDAN",
            "year": 2023,
            "car_make": car_make_instances[4],
            "dealer_id": 4,
        },
        {
            "name": "Camry",
            "type": "SEDAN",
            "year": 2023,
            "car_make": car_make_instances[4],
            "dealer_id": 10,
        },
        {
            "name": "Kluger",
            "type": "SUV",
            "year": 2023,
            "car_make": car_make_instances[4],
            "dealer_id": 1,
        },
    ]

    # Create CarModel instances
    for data in car_model_data:
        # Added dealer_id = 1 for missing field as required by the CarModel schema
        CarModel.objects.create(
            name=data["name"],
            car_make=data["car_make"],
            type=data["type"],
            year=data["year"],
            dealer_id=data.get("dealer_id", 1),  # Use explicit dealer_id from data
        )
