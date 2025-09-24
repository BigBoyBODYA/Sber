<template>
    <div class="container">
        <div class="history-container">
            <history-window/>
        </div>

        <div class="chat-container">
            <chat-window/>
        </div>

        <div class="button-container">
            <button-window/>
        </div>
    </div>
</template>

<script>
import ButtonWindow from '../components/buttonWindow.vue'
import ChatWindow from '../components/chatWindow.vue'
import HistoryWindow from '../components/historyWindow.vue'

export default {
    name: 'windowChat',

    components: {
        ButtonWindow,
        ChatWindow,
        HistoryWindow,
    },

    data() {
        return{
            
        }
    },

    methods:{

    },
}
</script>

<style>
.container{
    display: flex;
    width: 199vh;
    height: 98vh;
    
}

.history-container{
    width: 40vh;
    height: 98vh;
    background-color: red;
}

.chat-container{
    width: 120vh;
    height: 98vh;
    
}

.button-container{
    width: 39vh;
    height: 98vh;
    background-color: blueviolet;
}
</style>