import os
from Model.users import Users
from Persistence.data_manager import DataManager
from flask_bcrypt import generate_password_hash

def create_admin_user():
    data_manager = DataManager("database.json")
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'adminpassword')
    
    if not data_manager.get_by_field('email', admin_email, 'Users'):
        hashed_password = generate_password_hash(admin_password).decode('utf-8')
        admin_user = Users(email=admin_email, first_name='Admin', last_name='User', password=hashed_password)
        data_manager.save(admin_user)
        print('Admin user created')
    else:
        print('Admin user already exists')

if __name__ == '__main__':
    create_admin_user()
