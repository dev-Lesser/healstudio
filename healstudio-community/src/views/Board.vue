<template>
    <v-layout wrap class="board_page_layout">
        <v-flex xs12 sm8 md8>
            <v-card class="ma-3 pa-3" height=300>
            <v-card-title class="board_page_title">
                자유게시판
            </v-card-title>
            <v-divider />
                <v-list-item >
                    <div class="board_id_header">ID</div>
                    <div class="board_contents_header">제목</div>
                    <div class="board_user_header">작성자</div>
                    <div class="board_favorites_header">좋아요수</div>
                </v-list-item>
                <v-divider/>
                <div v-for="board, key in boards" :key="key">
                    <v-list-item :to="`/boards/${board.id}?user=${board.user}`" >
                        <div class="board_id">{{board.id}}</div>
                        <div class="board_contents">{{board.contents}}</div>
                        <div class="board_user">{{board.user}}</div>
                        <div class="board_favorites">{{board.favorites}}</div>
                    </v-list-item>
                    <v-divider/>
                </div>
                <div class="d-flex flex-row justify-center">
                    <v-icon class="pagination_page" @click="handlePrevClick" :color="start == 1 ? '#adadad' : '#757575'">mdi-chevron-left</v-icon>
                    <div class="pagination_page d-flex flex-row justify-center align-center" 
                        v-for="p in pages" :key="p" 
                        :class="{ selected_page: current == p }" 
                        @click="handlePageClick(p)">
                        {{ p }}
                    </div>
                    <v-icon class="pagination_page" @click="handleNextClick" :color="end == limit ? '#adadad' : '#757575'">mdi-chevron-right</v-icon>
                </div>
                <v-card-actions>
                    <v-btn :to="`/board/post`"> 글작성</v-btn>
                </v-card-actions>
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
            boards: null,
            pages: 5,
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
    font-family:'Jeju Gothic', sans-serif;
}
.board_page_title{
    font-size: 24px;
    font-family:'Jeju Gothic', sans-serif;
}
/* 게시물 CSS */
.board_id_header{
    width: 5%;
}
.board_id{
    width: 5%;
    font-size: 10px;
}
.board_contents_header{
    width: 70%;
}
.board_contents{
    width: 70%;
    font-size: 14px;
}
.board_user_header{
    width: 15%;
}
.board_user{
    width: 15%;
    font-size: 12px;
}
.board_favorites_header{
    width: 10%;
}
.board_favorites{
    width: 10%;
    font-size: 12px;
}




.pagination-bar {
        display: inline-block;
        padding-left: 0;
        margin: 20px 0;
        border-radius: 4px;
    }
.selected_page {
    color: white;
    background-color: #B2C9CF;
}
.pagination_page {
        cursor: pointer;
        width: 34px;
        height: 34px;
        border-radius: 17px;
        text-align: center;
        margin: 4px;
    }
.bottom_button{
    bottom: 1px;
}
</style>