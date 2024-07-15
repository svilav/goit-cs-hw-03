from pymongo import MongoClient, errors


client = MongoClient('mongodb://localhost:27017/')
db = client['cats_db']
collection = db['cats_collection']


def create_cat(name, age, features):
    """Створює новий запис про кота"""
    try:
        cat = {
            "name": name,
            "age": age,
            "features": features
        }
        result = collection.insert_one(cat)
        print(f"Кіт доданий з id: {result.inserted_id}")
    except errors.PyMongoError as e:
        print(f"Помилка при створенні запису: {e}")


def read_all_cats():
    """Виводить всі записи з колекції"""
    try:
        cats = collection.find()
        for cat in cats:
            print(cat)
    except errors.PyMongoError as e:
        print(f"Помилка при читанні записів: {e}")


def read_cat_by_name(name):
    """Виводить інформацію про кота за ім'ям"""
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"Кіт з ім'ям {name} не знайдений")
    except errors.PyMongoError as e:
        print(f"Помилка при читанні запису: {e}")


def update_cat_age(name, new_age):
    """Оновлює вік кота за ім'ям"""
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count:
            print(f"Вік кота з ім'ям {name} оновлений до {new_age}")
        else:
            print(f"Кіт з ім'ям {name} не знайдений")
    except errors.PyMongoError as e:
        print(f"Помилка при оновленні запису: {e}")


def add_feature_to_cat(name, new_feature):
    """Додає нову характеристику до списку features кота за ім'ям"""
    try:
        result = collection.update_one({"name": name}, {"$push": {"features": new_feature}})
        if result.matched_count:
            print(f"Нову характеристику додано до кота з ім'ям {name}")
        else:
            print(f"Кіт з ім'ям {name} не знайдений")
    except errors.PyMongoError as e:
        print(f"Помилка при оновленні запису: {e}")


def delete_cat_by_name(name):
    """Видаляє запис з колекції за ім'ям кота"""
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count:
            print(f"Кіт з ім'ям {name} видалений")
        else:
            print(f"Кіт з ім'ям {name} не знайдений")
    except errors.PyMongoError as e:
        print(f"Помилка при видаленні запису: {e}")


def delete_all_cats():
    """Видаляє всі записи з колекції"""
    try:
        result = collection.delete_many({})
        print(f"Видалено {result.deleted_count} записів")
    except errors.PyMongoError as e:
        print(f"Помилка при видаленні записів: {e}")


# Приклад використання функцій
if __name__ == "__main__":
    create_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    read_all_cats()
    read_cat_by_name("barsik")
    update_cat_age("barsik", 4)
    add_feature_to_cat("barsik", "грається з м'ячиками")
    delete_cat_by_name("barsik")
    delete_all_cats()
