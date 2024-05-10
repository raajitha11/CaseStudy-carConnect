import mysql.connector

from dao.interface.IAdminService import IAdminService
from exception.exceptions import AdminNotFoundException, InvalidInputException
from util.db_connection import DBConnection

class AdminService(IAdminService):
    def get_admin_by_id(self, admin_id):
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM admin WHERE adminID = %s", (admin_id,))
            admin = cursor.fetchone()
            cursor.close()
            if not admin:
                raise AdminNotFoundException(f"Admin with ID {admin_id} not found.")
            return admin
        except mysql.connector.Error as e:
            print("Error getting admin by id:", e)
            return None
        except AdminNotFoundException as e:
            print(e)
            return None
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def get_admin_by_username(self, username):
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM admin WHERE username = %s", (username,))
            admin = cursor.fetchone()
            cursor.close()
            if not admin:
                raise AdminNotFoundException(f"Admin with username {username} not found.")
            return admin
        except mysql.connector.Error as e:
            print("Error getting admin by username:", e)
            return None
        except AdminNotFoundException as e:
            print(e)
            return None
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def register_admin(self, admin):
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM admin WHERE username = %s", (admin.username,))
            count = cursor.fetchone()[0]

            if count > 0:
                raise InvalidInputException("Admin with that username already exists")
            cursor.execute("INSERT INTO admin (firstName, lastname, email, phoneNumber, username, password, role, joinDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (admin.first_name, admin.last_name, admin.email, admin.phone_number, admin.username, admin.password, admin.role, admin.join_date))
            connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print("Error registering admin:", e)
            return False
        except InvalidInputException as e:
            print(e)
            return False
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def update_admin(self, admin):
        try:
            adm = self.get_admin_by_id(admin.admin_id)
            if not adm:
                raise AdminNotFoundException(f"Admin with ID {admin.admin_id} not found")
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("SELECT adminID FROM admin WHERE username = %s", (admin.username,))
            existing_admin = cursor.fetchone()
            
            if existing_admin and existing_admin[0] != admin.admin_id:
                raise InvalidInputException("Admin with that username already exists")
            cursor.execute("UPDATE admin SET firstname = %s, lastname = %s, email = %s, phoneNumber = %s, username = %s, password = %s, role = %s WHERE adminID = %s",
                           (admin.first_name, admin.last_name, admin.email, admin.phone_number, admin.username, admin.password, admin.role, admin.admin_id))
            connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print("Error updating admin:", e)
            return False
        except AdminNotFoundException as e:
            print(e)
            return False
        except InvalidInputException as e:
            print(e)
            return False
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def delete_admin(self, admin_id):
        try:
            adm = self.get_admin_by_id(admin_id)
            if not adm:
                raise AdminNotFoundException(f"Admin with ID {admin_id} not found")
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM admin WHERE adminID = %s", (admin_id,))
            connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print("Error deleting admin:", e)
            return False
        except AdminNotFoundException as e:
            print(e)
            return False
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()
