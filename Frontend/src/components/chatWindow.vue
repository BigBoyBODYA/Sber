<template>
    <div class="chat-container">
        <!-- Заголовок чата -->
        <div class="chat-header">
            <h2>Чат с нейросетью</h2>
        </div>

        <!-- Область сообщений -->
        <div class="messages-container" ref="messagesContainer">
            <div 
                v-for="(message, index) in messages" 
                :key="index" 
                :class="['message', message.type]"
            >
                <div class="message-content">
                    {{ message.text }}
                </div>
                <div class="message-time">
                    {{ formatTime(message.timestamp) }}
                </div>
            </div>
        </div>

        <!-- Поле ввода и кнопки отправки -->
        <div class="input-container">
            <div class="input-wrapper">
                <input 
                    v-model="newMessage" 
                    @keyup.enter="sendMessage"
                    placeholder="Введите ваш запрос..."
                    class="message-input"
                    :disabled="isLoading"
                />

                <button 
                    @click="toggleVoiceInput"
                    :class="['voice-button', { 'recording': isRecording }]"
                    type="button"
                    :disabled="isLoading"
                    title="Голосовой ввод"
                >
                    <img 
                        v-if="!isRecording" 
                        :src="microphoneIcon" 
                        alt="Голосовой ввод" 
                        class="voice-icon"
                    />
                    <img 
                        v-else 
                        :src="recordingIcon" 
                        alt="Идет запись" 
                        class="voice-icon recording"
                    />
                </button>

                <button 
                    @click="sendMessage" 
                    :disabled="!newMessage.trim() || isLoading"
                    class="send-button"
                >
                    <span v-if="!isLoading">Отправить</span>
                    <span v-else>Отправка...</span>
                </button>
                
            </div>
            <!-- Индикатор голосового ввода -->
            <div v-if="isRecording" class="voice-status">
                Говорите... {{ recordingTime }}с
            </div>
        </div>
    </div>
</template>

<script>
import microphoneIcon from '../assets/microphone.svg';
import recordingIcon from '../assets/microphone.svg';

export default {
    name: 'ChatWindow',
    
    data() {
        return {
            messages: [
                {
                    text: 'Привет! Я нейросеть, готовая помочь вам. Задайте ваш вопрос!',
                    type: 'bot',
                    timestamp: new Date()
                }
            ],
            newMessage: '',
            isLoading: false,
            isRecording: false,
            recognition: null,
            recordingTime: 0,
            recordingTimer: null,
            microphoneIcon: microphoneIcon,
            recordingIcon: recordingIcon,
            apiUrl: 'http://localhost:5000/chat' // URL вашего локального сервера
        }
    },
    
    methods: {
        async sendMessage() {
            if (!this.newMessage.trim() || this.isLoading) return;

            // Добавляем сообщение пользователя
            const userMessage = {
                text: this.newMessage.trim(),
                type: 'user',
                timestamp: new Date()
            };
            
            this.messages.push(userMessage);
            const messageToSend = this.newMessage.trim();
            this.newMessage = ''; // Очищаем поле ввода сразу после отправки
            this.isLoading = true;
            
            // Прокрутка к нижней части чата
            this.$nextTick(() => {
                this.scrollToBottom();
            });

            try {
                // Отправка POST-запроса на локальный сервер
                const response = await fetch(this.apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: messageToSend
                    })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                
                // Добавляем ответ от нейросети
                const botMessage = {
                    text: data.response || data.message || 'Ответ от нейросети',
                    type: 'bot',
                    timestamp: new Date()
                };
                
                this.messages.push(botMessage);
                
            } catch (error) {
                console.error('Ошибка при отправке сообщения:', error);
                this.messages.push({
                    text: 'Произошла ошибка при обработке вашего запроса.',
                    type: 'bot',
                    timestamp: new Date()
                });
            } finally {
                this.isLoading = false;
                
                this.$nextTick(() => {
                    this.scrollToBottom();
                });
            }
        },
        
        // ОСНОВНАЯ ФУНКЦИЯ - ВКЛ/ВЫКЛ ПРИ ПОВТОРНОМ НАЖАТИИ
        toggleVoiceInput() {
            if (this.isRecording) {
                this.stopVoiceRecognition(); // ВЫКЛЮЧЕНИЕ при повторном нажатии
            } else {
                this.startVoiceRecognition(); // ВКЛЮЧЕНИЕ
            }
        },

        startVoiceRecognition() {
            // Проверка поддержки браузером
            if (!('webkitSpeechRecognition' in window)) {
                alert('Голосовой ввод не поддерживается вашим браузером');
                return;
            }

            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            
            // Минимальные настройки
            this.recognition.continuous = false;
            this.recognition.interimResults = true;
            this.recognition.lang = 'ru-RU';

            // Начало записи
            this.recognition.onstart = () => {
                this.isRecording = true;
                this.recordingTime = 0;
                this.recordingTimer = setInterval(() => {
                    this.recordingTime++;
                }, 1000);
            };

            // Получение результата
            this.recognition.onresult = (event) => {
                let transcript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    transcript += event.results[i][0].transcript;
                }
                this.newMessage = transcript;
            };

            // Ошибки
            this.recognition.onerror = (event) => {
                if (event.error === 'not-allowed') {
                    alert('Разрешите доступ к микрофону');
                }
                this.stopVoiceRecognition();
            };

            // Автозавершение (если браузер сам закончил запись)
            this.recognition.onend = () => {
                this.stopVoiceRecognition();
            };

            // Запуск
            this.recognition.start();
        },

        // ОТКЛЮЧЕНИЕ ЗАПИСИ - вызывается при повторном нажатии
        stopVoiceRecognition() {
            if (this.recognition) {
                this.recognition.stop();
            }
            this.isRecording = false;
            if (this.recordingTimer) {
                clearInterval(this.recordingTimer);
                this.recordingTimer = null;
            }
        },

        scrollToBottom() {
            const container = this.$refs.messagesContainer;
            if (container) {
                container.scrollTop = container.scrollHeight;
            }
        },
        
        formatTime(timestamp) {
            return timestamp.toLocaleTimeString('ru-RU', { 
                hour: '2-digit', 
                minute: '2-digit' 
            });
        }
    },
    
    mounted() {
        this.scrollToBottom();
    },

    beforeUnmount() {
        this.stopVoiceRecognition();
    }
}
</script>

<style scoped>
/* Стили остаются без изменений */
.chat-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    max-width: 1000px;
    margin: 0 auto;
    background-color: #f5f5f5;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    font-family: Helvetica;
}

.chat-header {
    background: linear-gradient(175deg,rgba(39, 179, 39, 1) 21%,
     rgba(87, 199, 133, 1) 60%, rgba(186, 242, 121, 1) 90%);
    color: white;
    padding: 15px 20px;
    text-align: center;
}

.chat-header h2 {
    margin: 0;
    font-size: 1.2rem;
}

.messages-container {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    max-height: 800px;
    background-color: white;
}

.message {
    margin-bottom: 15px;
    display: flex;
    flex-direction: column;
}

.message.user {
    align-items: flex-end;
}

.message.bot {
    align-items: flex-start;
}

.message-content {
    max-width: 70%;
    padding: 10px 15px;
    border-radius: 18px;
    word-wrap: break-word;
}

.message.user .message-content {
    background-color: #27B327;
    color: white;
    border-bottom-right-radius: 5px;
}

.message.bot .message-content {
    background-color: #e9ecef;
    color: #333;
    border-bottom-left-radius: 5px;
}

.message-time {
    font-size: 0.7rem;
    color: #666;
    margin-top: 5px;
}

.input-container {
    padding: 20px;
    background-color: white;
    border-top: 1px solid #e0e0e0;
}

.input-wrapper {
    display: flex;
    gap: 10px;
}

.message-input {
    flex: 1;
    padding: 12px 15px;
    border: 1px solid #ddd;
    border-radius: 25px;
    outline: none;
    font-size: 14px;
}

.message-input:focus {
    border-color: #4a90e2;
}

.message-input:disabled {
    background-color: #f5f5f5;
    cursor: not-allowed;
}

.send-button {
    padding: 12px 20px;
    background-color: #4a90e2;
    color: white;
    border: none;
    border-radius: 25px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
}

.send-button:hover:not(:disabled) {
    background-color: #357abd;
}

.send-button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

/* Анимация появления сообщений */
.message {
    animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Стили для скроллбара */
.messages-container::-webkit-scrollbar {
    width: 6px;
}

.messages-container::-webkit-scrollbar-track {
    background: #f1f1f1;
}

.messages-container::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
}

/* Стили для кнопки голосового ввода */
.voice-button {
    padding: 12px;
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 50%;
    cursor: pointer;
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.voice-button:hover:not(:disabled) {
    background-color: #e0e0e0;
    transform: scale(1.05);
}

.voice-button.recording {
    background-color: #ff4444;
    border-color: #ff4444;
}

.voice-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.voice-icon {
    width: 20px;
    height: 20px;
    object-fit: contain;
    transition: all 0.3s ease;
    /* Если SVG содержит встроенные цвета, можно инвертировать для hover */
    filter: brightness(0.5);
}

.voice-button:hover .voice-icon {
    transform: scale(1.1);
    filter: brightness(0.3);
}

.voice-button.recording .voice-icon {
    filter: brightness(0) invert(1); /* Делает иконку белой на красном фоне */
}

.voice-icon.recording {
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% {
        transform: scale(1);
        opacity: 1;
    }
    50% {
        transform: scale(1.2);
        opacity: 0.8;
    }
    100% {
        transform: scale(1);
        opacity: 1;
    }
}

.voice-status {
    text-align: center;
    margin-top: 8px;
    font-size: 12px;
    color: #666;
    font-style: italic;
}

.send-button {
    padding: 12px 20px;
    background-color: #4a90e2;
    color: white;
    border: none;
    border-radius: 25px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
    white-space: nowrap;
}
</style>