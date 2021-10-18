<template>
    <v-layout wrap class="board_page_layout">
        <v-flex xs12 sm8 md8>
            <v-card class="ma-3 pa-3" >
            <v-card-title class="board_page_title">
                자유게시판
            </v-card-title>
            <v-card-actions>
                <v-card-subtitle >
                    자유게시판 자유롭게 떠들어 제껴 봅시다. 공지사항 준수
                </v-card-subtitle>
                <v-spacer/>
                <v-card-actions>
                    <v-btn :to="`/board/post`" dark> 글작성</v-btn>
                </v-card-actions>
            </v-card-actions>
            <v-spacer/>
                    <v-text-field 
                        class="search-text-field"
                        v-model="query"
                        placeholder="검색" rounded outlined dense prepend-inner-icon="mdi-magnify"></v-text-field>
            <v-divider />
                <v-list-item >
                    <div class="board_id_header">ID</div>
                    <div class="board_contents_header">제목</div>
                    <div class="board_user_header">작성자</div>
                    <div class="board_favorites_header">좋아요수</div>
                </v-list-item>
                <v-divider/>
                    <v-list
                    class="board_list"
                    >   
                    <div v-for="board, key in boards" :key="key">
                        <v-list-item  v-if="key%2" dense :to="`/boards/${board.id}?user=${board.user}`" >
                            <div class="board_id">{{board.id}}</div>
                            <div class="board_contents">{{board.contents}}</div>
                            <div class="board_user">{{board.user}}</div>
                            <div class="board_favorites">{{board.favorites}}</div>
                        </v-list-item>
                        <v-list-item class="board_block_line" v-else dense :to="`/boards/${board.id}?user=${board.user}`" >
                            <div class="board_id">{{board.id}}</div>
                            <div class="board_contents">{{board.contents}}</div>
                            <div class="board_user">{{board.user}}</div>
                            <div class="board_favorites">{{board.favorites}}</div>
                        </v-list-item>
                        <v-divider/>
                    </div>
                    <div v-if="boards.length<15" >
                        <div v-for="i,key in 15-boards.length" :key="key">
                            <v-list-item dense>
                                <div class="board_no_contents"></div>
                            </v-list-item>
                            <v-divider/>
                        </div>
                    </div>
                    </v-list>
                
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
            query: null,
            boards: null,
            pages: 5,
            limit: 100,
            length: 15,
            end: 5,
            start:1,
            height: Math.round((window.innerHeight - 443) )
            // current: 1,
        }
    },
    async mounted(){
        if (this.$route.query.page == undefined || this.$route.query.page==1) await this.getBoards(0);
        else await this.getBoards((this.$route.query.page-1) * this.length)
    },
    methods:{
        async getBoards(skip){
            const [success, res] = await get_boards(skip)
            success;
            this.boards = res;
        },
        async handlePageClick(p){
            this.$store.state.current = p;
            this.$router.push(`/boards?page=${p}`)
            
        },
        async handlePrevClick(){
            if (this.start == 1)  return;
            this.$store.state.current = this.$store.state.current -1
            this.start = this.$store.state.current + this.pages
            this.end = this.start + this.pages
            this.$router.push(`/boards?page=${this.$store.state.current}`)
        },
        async handleNextClick(){
            if (this.end == this.limit)  return;
            this.$store.state.current = this.$store.state.current + 1
            this.start = this.$store.state.current - this.pages
            this.end = this.start + this.pages
            this.$router.push(`/boards?page=${this.$store.state.current}`)
        }
    },
    computed:{
        current(){
            return this.$store.state.current;
        }
    },
    watch:{
        current() {
            this.$router
                .push({
                query: {
                    page: this.current
                }
            })
            .catch(() => {
                console.log(this.current)
                this.getBoards((this.current-1)*this.length)
            });
    },
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
.board_block_line{
    background-color: #F0EEEE;
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