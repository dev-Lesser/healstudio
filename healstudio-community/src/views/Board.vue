<template>
    <v-layout wrap class="board_page_layout">
        
        <v-flex xs12 sm12 md12>
            <Meta :meta="meta"/>
        </v-flex>
        <v-flex xs12 sm10 md8>
            <v-card class="ma-3 pa-3" >
                <v-card-actions>
                <div class="board_page_title">
                    자유게시판
                </div>
                <v-spacer/>
                <v-btn @click="getBoardsReload"><v-icon dark>mdi-autorenew</v-icon>새로고침</v-btn>
                </v-card-actions>
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
                            
                            <div class="board_contents" v-if="!board.isDeleted">
                                {{board.title}}
                                <img class="board_new_img ml-2" v-if="isNew(board.created_at)[0]"  :src="newIcon">
                                <div class="board_reply_number">[{{board.replyNum}}]</div>
                            </div>
                            <div class="board_contents_deleted" v-else>{{board.title}}
                                <div class="board_reply_number">[{{board.replyNum}}]</div>
                            </div>
                            <div class="board_user">{{board.user}}</div>
                            <div class="board_favorites">{{board.favorites}}</div>
                            <div class="board_date">{{isNew(board.created_at)[1]}}</div>
                        </v-list-item>
                        <v-list-item class="board_block_line" v-else dense :to="`/boards/${board.id}?user=${board.user}`" >
                            <div class="board_id">{{board.id}}</div>
                            <div class="board_contents" v-if="!board.isDeleted">
                                {{board.title}}
                                <img class="board_new_img ml-2" v-if="isNew(board.created_at)[0]"  :src="newIcon">
                                <div class="board_reply_number">[{{board.replyNum}}]</div>
                            </div>
                            <div class="board_contents_deleted" v-else>
                                {{board.title}}
                                <div class="board_reply_number">[{{board.replyNum}}]</div>
                            </div>
                            <div class="board_user">{{board.user}}</div>
                            <div class="board_favorites">{{board.favorites}}</div>
                            <div class="board_date">{{isNew(board.created_at)[1]}}</div>
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
                :current-num="current"
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
    get_boards,
    get_boards_reload
} from '@/assets/board'
import newIcon from '@/assets/new.gif'
export default {
    components:{
        Meta,
        Pagination,
    },
    data() {
        return {
            newIcon: newIcon,
            now: new Date(),
            query: null,
            boards: null,
            page: this.$route.query.page!=undefined ? this.$route.query.page : 1,
            length: 12,
            height: Math.round((window.innerHeight - 443) ),
        }
    },
    async mounted(){
        if (this.$route.query.page == undefined || this.$route.query.page=='1') {
            this.$store.state.current = 1
            await this.getBoards(0, this.length, null);
        }
        else {
            this.$store.state.current = parseInt(this.$route.query.page)
            await this.getBoards((this.$route.query.page-1) * this.length, this.length, null)
        }
    },
    methods:{
        async pageClick(page) {
            this.page = page;
            this.$store.state.current = this.page
            
            await this.getBoards((this.page-1) * this.length,this.length, null);
        },
        async getBoards(skip, limit, user){
            const [success, res] = await get_boards(skip, limit, user)
            success;
            this.boards = res;
        },
        async getBoardsReload(){
            const [success, res] = await get_boards_reload((this.$store.state.current-1) * this.length, this.length, null, true);
            
            if (success){
                this.$store.state.meta.board = res.cnt
                this.boards = res.results
            }

        },
        isNew(date){
            const dateDiff =  this.now.getTime() - new Date(date).getTime()
            const diff = dateDiff/(1000*60)
            if (parseInt(diff)==0) return [true, '방금✨']
            if (0<= diff&& diff< 60) return [true, parseInt(diff) + '분전']
            if(60<= diff&& diff< 60*24) {
                return [true, parseInt(diff/60) + '시간전']
            }
            else return [false, date.split(' ')[0]]
        },

        
    },
    computed:{
        current(){
            return this.$store.state.current;
        },
        meta() {
            return this.$store.state.meta;
        },
        
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
    display:flex;
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
@media screen and (max-width: 768px) { 
    .board_date_header,.board_date,.board_favorites_header,.board_favorites { display: none; } 
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
    display:flex;
}
.board_reply_number{
    color: rgb(0, 0, 0);
    font-size: 11px;
    margin-left: 5px;
}
.board_new_img {
    width: 15px;
    height: 15px;
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