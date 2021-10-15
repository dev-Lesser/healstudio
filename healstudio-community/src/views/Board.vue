<template>
    <v-layout wrap class="board_page_layout">
        <v-flex xs12 sm8 md8>
            <v-card class="ma-3 pa-3" height=300>
            <v-card-title class="board_page_title">
                자유게시판
            </v-card-title>
            <v-divider />
                <div v-for="board, key in boards" :key="key" class="board_contents">
                    <v-list-item :to="`/board/${board.id}?user=${board.user}`" >
                        <div>{{board.user}}</div>
                        <div>{{board.contents}}</div>
                        <div>{{board.id}}</div>
                        <div>{{board.favorites}}</div>
                    </v-list-item>
                </div>
            </v-card>
        </v-flex>
    </v-layout>
</template>
<script>
import {
    get_boards
} from '@/assets/board'
export default {
    data() {
        return {
            boards: null
        }
    },
    async created(){
        await this.getBoards(0);
    },
    methods:{
        async getBoards(skip){
            const [success, res] = await get_boards(skip)
            success;
            this.boards = res;
        }
    }
}
</script>
<style scoped>
.board_page_layout{
    display: flex;
    justify-content: center;
}
.board_page_title{
    font-size: 24px;
    font-family:'Jeju Gothic', sans-serif;
}   
</style>