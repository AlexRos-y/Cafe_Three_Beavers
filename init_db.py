from app import create_app
from models import db, User, Category, MenuItem
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Очищаем базу (только для разработки!)
    db.drop_all()
    db.create_all()
    
    # Создаём админа
    admin = User(
        username='admin',
        email='admin@cafe.ru',
        password_hash=generate_password_hash('admin123'),
        is_admin=True
    )
    db.session.add(admin)
    
    # Создаём тестового пользователя
    user = User(
        username='user',
        email='user@cafe.ru',
        password_hash=generate_password_hash('user123')
    )
    db.session.add(user)
    
    db.session.commit()
    
    print("✅ База данных инициализирована!")
    print("📧 Админ: admin@cafe.ru / admin123")
    print("📧 Пользователь: user@cafe.ru / user123")