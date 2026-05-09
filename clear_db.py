from app import create_app
from models import db

app = create_app()

with app.app_context():
    # Удаляем все записи из всех таблиц
    db.drop_all()
    db.create_all()
    
    print("✅ База данных полностью очищена!")
    print("Теперь запусти: python init_db.py")