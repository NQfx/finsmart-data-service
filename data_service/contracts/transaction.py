from enum import StrEnum
from dataclasses import dataclass

@dataclass(frozen=True)
class Transaction:
    is_positive: bool 
    category: Category
    datetime: datetime
    amount: float
    remaining: float
    desc: str

class TransactionCategory(StrEnum):
    AUTO = "auto"
    GAS_STATION = "gas-station"
    PHARMACY = "pharmacy"
    BUSINESS_SERVICES = "business-services"
    CHARITY = "charity"
    HOUSEHOLD_SERVICES = "household-services"
    GOVERNMENT_PAYMENTS = "government-payments"
    FOOD_DELIVERY = "food-delivery"
    UTILITIES = "utilities"
    ART = "art"
    RESTAURANTS_CAFES = "restaurants-cafes"
    CINEMA_THEATRE = "cinema-theatre"
    COMMISSION = "commission"
    LOANS = "loans"
    GAMBLING = "gambling"
    MARKETPLACES = "marketplaces"
    MEDICAL_SERVICES = "medical-services"
    INVESTMENT = "investment"
    EDUCATION = "education"
    CLOTHING_SHOES = "clothing-shoes"
    WHOLESALE = "wholesale"
    PERFUME_COSMETICS = "perfume-cosmetics"
    PERSON_TRANSFERS = "person-transfers"
    TRANSPORT_DELIVERY = "transport-delivery"
    PETS = "pets"
    SUBSCRIPTIONS = "subscriptions"
    HOUSING = "housing"
    OTHERS = "others"
    TRAVEL = "travel"
    BEAUTY_SALONS = "beauty-salons"
    SELF_EMPLOYMENT = "self-employment"
    CASH_WITHDRAWAL = "cash-withdrawal"
    SPORTS_FITNESS = "sports-fitness"
    SUPERMARKETS = "supermarkets"
    TOBACCO_STORES = "tobacco-stores"
    TAXI_CAR_SHARING = "taxi-car-sharing"
    KIDS_PRODUCTS = "kids-products"
    HOME_PRODUCTS = "home-products"
    VEHICLE = "vehicle"
    INSURANCE = "insurance"
    HOBBIES = "hobbies"
    MEMBERSHIP = "membership"
    ELECTRONICS = "electronics"
    JEWELRY = "jewelry"
    TRANSFERS = "transfers"
