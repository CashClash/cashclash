import os
import json


def update_image_extensions(directory):
    if not os.path.exists(directory):
        print(f"Помилка: Шлях {directory} не знайдено.")
        return

    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    updated_files_count = 0

    for filename in json_files:
        file_path = os.path.join(directory, filename)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Прапорець, щоб знати, чи були зміни у цьому файлі
            changes_made = [False]

            # Рекурсивна функція для заміни значень
            def walk_and_replace(obj):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        if key == "image" and isinstance(value, str):
                            # Перевіряємо, чи це не svg і не вже webp
                            if not value.lower().endswith('.svg') and not value.lower().endswith('.webp'):
                                # Замінюємо розширення на .webp
                                base_path = os.path.splitext(value)[0]
                                obj[key] = base_path + ".webp"
                                changes_made[0] = True
                        else:
                            walk_and_replace(value)
                elif isinstance(obj, list):
                    for item in obj:
                        walk_and_replace(item)

            walk_and_replace(data)

            # Якщо були зміни, перезаписуємо файл
            if changes_made[0]:
                with open(file_path, 'w', encoding='utf-8') as f:
                    # ensure_ascii=False зберігає кирилицю, indent=2 для гарного форматування
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"Оновлено посилання у файлі: {filename}")
                updated_files_count += 1

        except Exception as e:
            print(f"Помилка при обробці файлу {filename}: {e}")

    print(f"\nРоботу завершено! Оновлено файлів: {updated_files_count}")


# Шлях до папки з англійською датою
data_dir = r"D:\Python\cashclash.github.io\ua\data"
update_image_extensions(data_dir)