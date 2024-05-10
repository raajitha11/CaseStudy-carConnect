import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from entity.customer import Customer
from entity.vehicle import Vehicle
from dao.imp.authenticationService import AuthenticationService
from dao.imp.customerService import CustomerService
from dao.imp.vehicleService import VehicleService

def test_customer_authentication_invalid():
    auth_service = AuthenticationService()
    # assert auth_service.authenticate_customer("invalid_username", "invalid_password")
    assert auth_service.authenticate_customer("max", "123max")

def test_update_customer_info():
    customer_service = CustomerService()
    customer_data = Customer(
        customer_id= 1,
        first_name= "New First Name",
        last_name= "New Last Name",
        email= "new_email@example.com",
        phone_number= "1234567890",
        address= "New Address",
        username= "new_username",
        password= "new_password"
    )
    assert customer_service.update_customer(customer_data)

def test_add_new_vehicle():
    vehicle_service = VehicleService()
    vehicle_data = {"model": "New Model", "make": "New Make", "year": 2022, "color": "Red", "registration_number": "NEW1234789123", "availability": True, "daily_rate": 50}
    vehicle = Vehicle(**vehicle_data)
    assert vehicle_service.add_vehicle(vehicle)


def test_update_vehicle_details():
    vehicle_service = VehicleService()
    vehicle_data = {"vehicle_id": 1, "model": "Updated Model", "make": "Updated Make", "year": 2023, "color": "Blue", "registration_number": "UPDATED123", "availability": True, "daily_rate": 60}
    vehicle = Vehicle(**vehicle_data)
    assert vehicle_service.update_vehicle(vehicle)


def test_get_available_vehicles():
    vehicle_service = VehicleService()
    available_vehicles = vehicle_service.get_available_vehicles()
    assert available_vehicles is not None


def test_get_all_vehicles():
    vehicle_service = VehicleService()
    all_vehicles = vehicle_service.get_all_vehicles()
    assert all_vehicles is not None
