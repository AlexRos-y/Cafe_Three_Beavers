from app import create_app
from models import db, User, Category, MenuItem, Review
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Очищаем базу (только для разработки!)
    db.drop_all()
    db.create_all()
    
    # === ПОЛЬЗОВАТЕЛИ ===
    admin = User(
        username='admin',
        email='admin@cafe.ru',
        password_hash=generate_password_hash('admin123'),
        is_admin=True
    )
    db.session.add(admin)
    
    user = User(
        username='user',
        email='user@cafe.ru',
        password_hash=generate_password_hash('user123')
    )
    db.session.add(user)
    
    anna = User(
        username='Анна',
        email='anna@mail.ru',
        password_hash=generate_password_hash('anna123')
    )
    db.session.add(anna)
    
    mikhail = User(
        username='Михаил',
        email='mikhail@mail.ru',
        password_hash=generate_password_hash('mikhail123')
    )
    db.session.add(mikhail)
    
    ekaterina = User(
        username='Екатерина',
        email='ekaterina@mail.ru',
        password_hash=generate_password_hash('katya123')
    )
    db.session.add(ekaterina)
    
    db.session.commit()  # Сохраняем пользователей, чтобы получить их ID
    
    # === КАТЕГОРИИ МЕНЮ ===
    categories = [
        Category(name='Горячие блюда'),
        Category(name='Салаты'),
        Category(name='Супы'),
        Category(name='Десерты'),
        Category(name='Напитки'),
        Category(name='Закуски')
    ]
    db.session.add_all(categories)
    db.session.commit()
    
    # === БЛЮДА МЕНЮ ===
    menu_items = [
        # Горячие блюда (category_id=1)
        MenuItem(name='Стейк из лосося', description='Нежнейший стейк из норвежского лосося с овощами гриль и соусом терияки', price=1200, category_id=1),
        MenuItem(name='Паста Карбонара', description='Классическая итальянская паста с беконом, яйцом и пармезаном', price=850, category_id=1),
        MenuItem(name='Куриная грудка гриль', description='Сочная куриная грудка с пряными травами и картофельным пюре', price=750, category_id=1),
        MenuItem(name='Утиная ножка конфи', description='Утиная ножка, томлёная в собственном соку, с карамелизированными яблоками', price=1350, category_id=1),
        
        # Салаты (category_id=2)
        MenuItem(name='Цезарь с курицей', description='Классический салат с куриной грудкой, пармезаном и гренками', price=650, category_id=2),
        MenuItem(name='Греческий салат', description='Свежие овощи, маслины, сыр фета с оливковым маслом', price=550, category_id=2),
        MenuItem(name='Салат с ростбифом', description='Тонко нарезанный ростбиф с рукколой, помидорами черри и бальзамическим соусом', price=780, category_id=2),
        
        # Супы (category_id=3)
        MenuItem(name='Тыквенный крем-суп', description='Нежный крем-суп из тыквы с имбирём и кокосовым молоком', price=450, category_id=3),
        MenuItem(name='Борщ с говядиной', description='Традиционный борщ с говядиной, сметаной и чесночными пампушками', price=550, category_id=3),
        MenuItem(name='Том-ям', description='Острый тайский суп с креветками, грибами и кокосовым молоком', price=680, category_id=3),
        
        # Десерты (category_id=4)
        MenuItem(name='Чизкейк Нью-Йорк', description='Классический чизкейк на песочной основе с ягодным соусом', price=450, category_id=4),
        MenuItem(name='Тирамису', description='Итальянский десерт с маскарпоне, кофе и какао', price=520, category_id=4),
        MenuItem(name='Шоколадный фондан', description='Горячий шоколадный десерт с жидкой сердцевиной и шариком ванильного мороженого', price=480, category_id=4),
        
        # Напитки (category_id=5)
        MenuItem(name='Капучино', description='Классический кофе с молочной пенкой', price=250, category_id=5),
        MenuItem(name='Латте матча', description='Японский зелёный чай матча с молоком', price=320, category_id=5),
        MenuItem(name='Лимонад домашний', description='Освежающий лимонад с мятой и лаймом', price=280, category_id=5),
        MenuItem(name='Смузи ягодный', description='Густой смузи из свежих ягод с бананом', price=350, category_id=5),
        
        # Закуски (category_id=6)
        MenuItem(name='Брускетта с томатами', description='Хрустящий хлеб с помидорами, базиликом и чесноком', price=420, category_id=6),
        MenuItem(name='Сырная тарелка', description='Ассорти из 4 видов сыра с мёдом, орехами и виноградом', price=890, category_id=6),
        MenuItem(name='Креветки в темпуре', description='Хрустящие креветки с соусом сладкий чили', price=650, category_id=6),
    ]
    db.session.add_all(menu_items)
    db.session.commit()
    
    # === ОТЗЫВЫ ===
    reviews_data = [
        Review(
            user_id=3,  # Анна
            rating=5,
            text='Прекрасное место! Очень уютная атмосфера, вкусная еда и приветливый персонал. Обязательно вернёмся сюда снова. Особенно понравился стейк из лосося — просто тает во рту!',
            created_at=datetime.utcnow() - timedelta(days=2)
        ),
        Review(
            user_id=4,  # Михаил
            rating=4,
            text='Хорошее кафе с авторской кухней. Цены немного выше среднего, но оно того стоит. Брал пасту карбонара — очень вкусно. Единственное, долго ждали заказ, но это был вечер пятницы.',
            created_at=datetime.utcnow() - timedelta(days=5)
        ),
        Review(
            user_id=5,  # Екатерина
            rating=5,
            text='Отмечали здесь день рождения подруги. Очень понравилось обслуживание, заранее украсили столик, принесли комплимент от шеф-повара. Чизкейк просто божественный!',
            created_at=datetime.utcnow() - timedelta(days=7)
        ),
    ]
    db.session.add_all(reviews_data)
    db.session.commit()
    
    print("✅ База данных инициализирована с демо-данными!")
    print("\n👥 Пользователи:")
    print("  📧 admin@cafe.ru / admin123 (админ)")
    print("  📧 user@cafe.ru / user123")
    print("  📧 anna@mail.ru / anna123")
    print("  📧 mikhail@mail.ru / mikhail123")
    print("  📧 ekaterina@mail.ru / katya123")
    print(f"\n🍽️ Добавлено {len(menu_items)} блюд в меню")
    print(f"📁 Категории: {', '.join([c.name for c in categories])}")
    print(f"⭐ Добавлено {len(reviews_data)} отзыва")