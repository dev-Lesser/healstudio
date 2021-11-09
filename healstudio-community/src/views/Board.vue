<template>
    <v-layout wrap class="board_page_layout">
        
        <v-flex xs12 sm12 md12>
            <Meta :meta="meta"/>
        </v-flex>
        <v-flex xs12 sm8 md8>
            <v-card class="ma-3 pa-3" >
            <div class="board_page_title">
                자유게시판
            </div>
            <v-card-actions>
                <v-card-subtitle >
                    자유게시판 자유롭게 떠들어 제껴 봅시다. 공지사항 준수
                </v-card-subtitle>
                <v-spacer/>
                <v-card-actions>
                    <v-btn :to="`/board/post`" dark> 글 작성</v-btn>
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
                    <div class="board_favorites_header"><v-icon small color="rgb(128, 140, 247)">mdi-thumb-up</v-icon></div>
                    <div class="board_date_header">작성일</div>
                </v-list-item>
                <v-divider/>
                    <v-list
                    class="board_list"
                    >   
                    <div v-for="board, key in boards" :key="key">
                        <v-list-item  v-if="key%2" dense :to="`/boards/${board.id}?user=${board.user}`" >
                            <div class="board_id" >{{board.id}}</div>
                            
                            <div class="board_contents" v-if="!board.isDeleted">{{board.title}}</div>
                            <div class="board_contents_deleted" v-else>{{board.title}}</div>
                            <div class="board_user">{{board.user}}</div>
                            <div class="board_favorites">{{board.favorites}}</div>
                            <div class="board_date">{{board.created_at}}</div>
                        </v-list-item>
                        <v-list-item class="board_block_line" v-else dense :to="`/boards/${board.id}?user=${board.user}`" >
                            <div class="board_id">{{board.id}}</div>
                            <div class="board_contents" v-if="!board.isDeleted">{{board.title}}</div>
                            <div class="board_contents_deleted" v-else>{{board.title}}</div>
                            <div class="board_user">{{board.user}}</div>
                            <div class="board_favorites">{{board.favorites}}</div>
                            <div class="board_date">{{board.created_at}}</div>
                        </v-list-item>
                        <v-divider/>
                    </div>
                    <div v-if="boards!=null && boards.length<length" >
                        <div v-for="i,key in length-boards.length" :key="key">
                            <v-list-item dense>
                                <div class="board_no_contents"></div>
                            </v-list-item>
                            <v-divider/>
                        </div>
                    </div>
                    </v-list>
                
                <Pagination 
                @page-click="pageClick"
                :total="meta.board"
                :length="12"
                />
                
            </v-card>
        </v-flex>
    </v-layout>
</template>
<script>
import Meta from '@/components/board/Meta'
import Pagination from '@/components/Pagination'
import {
    get_boards
} from '@/assets/board'
export default {
    components:{
        Meta,
        Pagination,
    },
    data() {
        return {
            query: null,
            boards: null,
            page: this.$route.query.page!=undefined ? this.$route.query.page : 1,
            limit: 5,
            length: 12,
            end: 5,
            start: this.$store.state.current,
            height: Math.round((window.innerHeight - 443) ),
            
            // current: 1,
        }
    },
    async mounted(){
        if (this.$route.query.page == undefined || this.$route.query.page==1) {
            await this.getBoards(0, this.length, null);
        }
        else {
            this.$store.state.current = this.$route.query.page;
            await this.getBoards((this.$route.query.page-1) * this.length, this.length, null)
        }
    },
    methods:{
        async pageClick(page) {
            this.page = page;
            await this.getBoards((this.page-1) * this.length,this.length, null);
        },
        async getBoards(skip, limit, user){
            const [success, res] = await get_boards(skip, limit, user)
            success;
            this.boards = res;
        },
    },
    computed:{
        current(){
            return this.$store.state.current;
        },
        meta() {
                return this.$store.state.meta;
        }
        
    },


}
</script>
<style scoped>

.board_page_layout{
    display: flex;
    justify-content: center;
    align-items: center;
    font-family:'Jeju Gothic', sans-serif;
}
.board_adv_values{
    display: flex;
    padding: 30px;
    justify-content: center;
    align-items: center;
    text-align: center;
}
.board_page_title{
    font-size: 25px;
    margin-top: 10px;
    margin-left: 20px;
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
.board_date_header,
.board_date{
    width: 10%;
}
.board_date{
    font-size: 12px;
}
.board_block_line{
    background-color: #F0EEEE;
}
.board_contents_deleted{
    color: rgb(252, 166, 166);
    width: 70%;
    font-size:11px;
}



.pagination-bar {
        display: inline-block;
        padding-left: 0;
        margin: 20px 0;
        border-radius: 4px;
    }
.selected_page {
    color: white;
    background-color: #849599;
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