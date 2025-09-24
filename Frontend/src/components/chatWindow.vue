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

        <!-- Поле ввода и кнопка отправки -->
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
                    @click="sendMessage" 
                    :disabled="!newMessage.trim() || isLoading"
                    class="send-button"
                >
                    <span v-if="!isLoading">Отправить</span>
                    <span v-else>Отправка...</span>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
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
            isLoading: false
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
            this.newMessage = '';
            this.isLoading = true;
            
            // Прокрутка к нижней части чата
            this.$nextTick(() => {
                this.scrollToBottom();
            });

            try {
                // Здесь будет вызов к API нейросети
                // Временно имитируем ответ
                setTimeout(() => {
                    const botMessage = {
                        text: `Это имитация ответа нейросети на ваш запрос: "${messageToSend}". В реальном приложении здесь будет ответ от API.`,
                        type: 'bot',
                        timestamp: new Date()
                    };
                    
                    this.messages.push(botMessage);
                    this.isLoading = false;
                    
                    this.$nextTick(() => {
                        this.scrollToBottom();
                    });
                }, 1000);
                
            } catch (error) {
                console.error('Ошибка при отправке сообщения:', error);
                this.messages.push({
                    text: 'Произошла ошибка при обработке вашего запроса.',
                    type: 'bot',
                    timestamp: new Date()
                });
                this.isLoading = false;
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
    }
}
</script>

<style scoped>
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
    font-family: 'Sans', sans-serif;
}

.chat-header {
    background-color: #4a90e2;
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
    background-color: #4a90e2;
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
</style>