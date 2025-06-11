# 🛒 Store Inventory System

Учёт поступлений товаров для магазинов — тестовое задание с использованием Django, Django Ninja и Unfold Admin.

## 🚀 Технологии

- Python 3.11+
- Django 5.0+
- Django Ninja
- Django Unfold
- SQLite

## 📦 Установка и запуск


```bash
git clone https://github.com/meruauez/store_inventory.git
cd store_inventory
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

