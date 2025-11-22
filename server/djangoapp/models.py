from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.timezone import \
    now  # Added for potential future use or consistency


# <HINT> Create a Car Make model
class CarMake(models.Model):
    """
    Represents a car manufacturer (e.g., Ford, Toyota).
    Stores basic information about the car make.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    # Custom field for optional branding information
    country_of_origin = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        """Returns the string representation of the CarMake object."""
        return self.name


# <HINT> Create a Car Model model
class CarModel(models.Model):
    """
    Represents a specific car model (e.g., F-150, Camry).
    Links to a CarMake and includes details like type, year, and dealer reference.
    """

    # Many-to-one relationship to CarMake
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    # Dealer ID referring to a dealer in the external Cloudant database
    dealer_id = models.IntegerField(help_text="Dealer ID from the external database")

    name = models.CharField(max_length=100)

    # Choices for car type
    CAR_TYPES = [
        ("SEDAN", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "Wagon"),
        ("TRUCK", "Truck"),
        ("SPORTS", "Sports Car"),
    ]
    type = models.CharField(
        max_length=10,
        choices=CAR_TYPES,
        default="SUV",
        help_text="Select car body type",
    )

    # Year field with specified validators
    current_year = now().year
    year = models.IntegerField(
        default=current_year,
        validators=[
            MaxValueValidator(current_year),  # Use current year dynamically
            MinValueValidator(2015),
        ],
        help_text="Year of the model (2015-2023)",
    )

    def __str__(self):
        """Returns the string representation of the CarModel object."""
        # Print a combination of Make and Model name for clarity
        return f"{self.car_make.name} - {self.name} ({self.year})"
