# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from neyro import GigaChatManager
import time

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех доменов

# Инициализация менеджера GigaChat
API_TOKEN = 'MDE5OTc1YzktMTIxZS03NTM1LWEzNDYtNTUyY2Y4ZTMzYzg2OjcwYWJmNTM2LTI0YWEtNGJhMi05N2ZiLWU3YzQzNTVmYWEzYw=='
giga_manager = GigaChatManager(API_TOKEN)


def ask_according_to_material_fixed(message: str) -> str:
    """
    Исправленная функция для запроса к нейросети без использования attachments
    """
    try:
        # Создаем промпт с указанием контекста
        prompt = f"""Ты - эксперт в области инженерии и машиностроения. 
Ты в полной мере владеешь материалом и терминами, ты не пользуешься условными обозначениями, 
а используешь в своей речи наименования материалов или инструментала, с которым работаешь.

Отвечай на основе загруженных в тебя технических документов.

Вопрос: {message}

Ответь технически грамотно:"""

        # Отправляем запрос без attachments
        result = giga_manager.giga.chat({
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                    "attachments": ["620c1733-7d34-462d-8ff2-391a19cca465"], # Это индекс учебника BASE.PDF
                }
            ],
            "temperature": 0.1
        })

        # Извлекаем ответ
        if hasattr(result, 'choices') and len(result.choices) > 0:
            return result.choices[0].message.content
        elif hasattr(result, 'message') and hasattr(result.message, 'content'):
            return result.message.content
        else:
            return "Не удалось получить ответ от нейросети"

    except Exception as e:
        print(f"Ошибка в ask_according_to_material_fixed: {e}")
        return f"Произошла ошибка при обращении к нейросети: {str(e)}"


@app.route('/chat', methods=['POST'])
def chat_with_ai():
    """
    Обработчик POST-запроса для общения с нейросетью
    """
    try:
        # Получаем данные из запроса
        data = request.get_json()

        # Проверяем наличие сообщения
        if not data or 'message' not in data:
            return jsonify({'error': 'Сообщение обязательно'}), 400

        user_message = data['message']

        # Проверяем, что сообщение не пустое
        if not user_message.strip():
            return jsonify({'error': 'Сообщение не может быть пустым'}), 400

        print(f"Получен запрос: {user_message}")

        # Вызываем исправленную функцию
        start_time = time.time()
        ai_response = ask_according_to_material_fixed(user_message)
        processing_time = time.time() - start_time

        print(f"Ответ от нейросети получен за {processing_time:.2f} сек")
        print(f"Ответ: {ai_response}")

        # Возвращаем ответ
        return jsonify({
            'response': ai_response,
            'status': 'success',
            'processing_time': f"{processing_time:.2f} сек"
        })

    except Exception as e:
        print(f"Ошибка при обработке запроса: {e}")
        return jsonify({
            'error': f'Внутренняя ошибка сервера: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка работоспособности сервера"""
    try:
        # Проверяем подключение к GigaChat
        files_count = len(giga_manager.files)
        return jsonify({
            'status': 'OK',
            'message': 'Сервер работает',
            'files_available': files_count
        })
    except Exception as e:
        return jsonify({
            'status': 'ERROR',
            'message': f'Ошибка подключения к GigaChat: {str(e)}'
        }), 500


@app.route('/api/files', methods=['GET'])
def get_files_info():
    """Получение информации о загруженных файлах"""
    try:
        files = giga_manager.files
        files_info = [
            {
                'index': file.index,
                'id': file.id,
                'name': file.fullname
            }
            for file in files
        ]
        return jsonify({
            'files': files_info,
            'total_count': len(files)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Запускаем сервер на localhost:5000
    print("Запуск сервера на http://localhost:5000")
    print("Доступные эндпоинты:")
    print("  POST /api/chat - для общения с нейросетью")
    print("  GET  /api/health - для проверки работоспособности")
    print("  GET  /api/files - для получения информации о файлах")

    # Проверяем подключение к GigaChat
    try:
        files = giga_manager.files
        print(f"Подключение к GigaChat успешно. Доступно файлов: {len(files)}")
        for file in files:
            print(f"  - {file.fullname} (ID: {file.id})")
    except Exception as e:
        print(f"Ошибка подключения к GigaChat: {e}")

    app.run(host='0.0.0.0', port=5000, debug=True)