
import mysql.connector

from dao.interface.ICustomerService import ICustomerService
from exception.exceptions import CustomerNotFoundException, InvalidInputException
from util.db_connection import DBConnection

class CustomerService(ICustomerService):

    def get_customer_by_id(self, customer_id):
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM customer WHERE customerID = %s", (customer_id,))
            customer = cursor.fetchone()
            cursor.close()
            if not customer:
                raise CustomerNotFoundException(f"Customer not found with ID {customer_id}")
            return customer
        except mysql.connector.Error as e:
            print("Error getting customer by id:", e)
            return None
        except CustomerNotFoundException as e:
            print(e)
            return None
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def get_customer_by_username(self, username):
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM customer WHERE username = %s", (username,))
            customer = cursor.fetchone()
            cursor.close()
            if not customer:
                raise CustomerNotFoundException(f"Customer not found with username {username}")
            return customer
        except mysql.connector.Error as e:
            print("Error getting customer by username:", e)
            return None
        except CustomerNotFoundException as e:
            print(e)
            return None
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def register_customer(self, customer):
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM customer WHERE username = %s", (customer.username,))
            count = cursor.fetchone()[0]

            if count > 0:
                raise InvalidInputException("A customer with that username already exists")
            cursor.execute("INSERT INTO customer (firstname, lastname, email, phoneNumber, address, username, password, registrationDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (customer.first_name, customer.last_name, customer.email, customer.phone_number, customer.address, customer.username, customer.password, customer.registration_date))
            connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print("Error registering customer:", e)
            return False
        except InvalidInputException as e:
            print(e)
            return False
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def update_customer(self, customer):
        try:
            cust = self.get_customer_by_id(customer.customer_id)
            if not cust:
                raise CustomerNotFoundException(message=f"customer with {customer.customer_id} not found.")
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("SELECT customerID FROM customer WHERE username = %s", (customer.username,))
            existing_cust = cursor.fetchone()
            
            if existing_cust and existing_cust[0] != customer.customer_id:
                raise InvalidInputException("A customer with that username already exists")
            cursor.execute("UPDATE customer SET firstname = %s, lastname = %s, email = %s, phoneNumber = %s, address = %s, username = %s, password = %s WHERE customerID = %s",
                           (customer.first_name, customer.last_name, customer.email, customer.phone_number, customer.address, customer.username, customer.password, customer.customer_id))
            connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print("Error updating customer:", e)
            return False
        except InvalidInputException as e:
            print(e)
            return False
        except CustomerNotFoundException as e:
            print(e)
            return False
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def delete_customer(self, customer_id):
        try:
            cust = self.get_customer_by_id(customer_id)
            if not cust:
                raise CustomerNotFoundException(message=f"customer with {customer_id} not found.")
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM customer WHERE customerID = %s", (customer_id,))
            connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            if e.errno == 1451:
                print("Cannot delete customer. There are reservations associated with this customer.")
            else:
                print("Error deleting customer:", e)
            return False
        except CustomerNotFoundException as e:
            print(e)
            return False
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()
