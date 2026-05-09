from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User
from forms import LoginForm, RegisterForm, ProfileForm
from PIL import Image, ImageDraw, ImageFont
import os
import uuid
import io

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/avatar/<int:user_id>')
def avatar(user_id):
    """Отдаёт аватар пользователя"""
    user = User.query.get_or_404(user_id)
    
    if user.avatar and user.avatar != 'default-avatar.png':
        avatar_path = os.path.join(current_app.static_folder, 'uploads', 'avatars', user.avatar)
        if os.path.exists(avatar_path):
            return send_file(avatar_path)
    
    first_letter = user.username[0].upper() if user.username else '?'
    
    colors = {
        'А': (33, 150, 243), 'Б': (244, 67, 54), 'В': (76, 175, 80),
        'Г': (255, 152, 0), 'Д': (156, 39, 176), 'Е': (0, 188, 212),
        'Ж': (255, 87, 34), 'З': (63, 81, 181), 'И': (139, 195, 74),
        'К': (233, 30, 99), 'Л': (0, 150, 136), 'М': (121, 85, 72),
        'Н': (255, 193, 7), 'О': (158, 158, 158), 'П': (96, 125, 139),
        'Р': (205, 220, 57), 'С': (3, 169, 244), 'Т': (255, 235, 59),
        'У': (103, 58, 183), 'Ф': (233, 30, 99), 'Х': (0, 96, 100),
        'Ц': (230, 81, 0), 'Ч': (194, 24, 91), 'Ш': (46, 125, 50),
        'Щ': (21, 101, 192), 'Э': (245, 124, 0), 'Ю': (56, 142, 60),
        'Я': (191, 54, 12),
    }
    
    bg_color = colors.get(first_letter, (45, 90, 39))
    
    size = 150
    img = Image.new('RGB', (size, size), color=bg_color)
    draw = ImageDraw.Draw(img)

    draw.ellipse([0, 0, size-1, size-1], fill=bg_color)

    try:
        font = ImageFont.truetype("arial.ttf", 70)
    except:
        try:
            font = ImageFont.truetype("arialbd.ttf", 70)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 70)
            except:
                font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), first_letter, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (size - w) // 2
    y = (size - h) // 2 - h // 4
    
    draw.text((x, y), first_letter, fill=(255, 255, 255), font=font)
    
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=True)
            flash('Вы успешно вошли в систему!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Неверный email или пароль', 'danger')
    
    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash('Пароли не совпадают', 'danger')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Пользователь с таким email уже существует', 'danger')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(username=form.username.data).first():
            flash('Пользователь с таким именем уже существует', 'danger')
            return render_template('register.html', form=form)
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    
    if form.validate_on_submit():
        if form.avatar.data:
            avatar_file = form.avatar.data
            unique_name = f"{uuid.uuid4().hex}_{secure_filename(avatar_file.filename)}"
            
            upload_folder = os.path.join(current_app.static_folder, 'uploads', 'avatars')
            os.makedirs(upload_folder, exist_ok=True)
            
            filepath = os.path.join(upload_folder, unique_name)
            avatar_file.save(filepath)
            
            if current_user.avatar and current_user.avatar != 'default-avatar.png':
                old_file = os.path.join(upload_folder, current_user.avatar)
                if os.path.exists(old_file):
                    os.remove(old_file)
            
            current_user.avatar = unique_name
            db.session.commit()
            
            flash('Аватар успешно обновлён!', 'success')
        else:
            flash('Выберите изображение для загрузки', 'warning')
    
    return render_template('profile.html', form=form)