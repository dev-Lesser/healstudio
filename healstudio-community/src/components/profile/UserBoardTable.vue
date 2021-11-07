<template>
    <v-card class="pa-3 ma-3">
        
        <div>
            <v-card-title>
                최근 작성글
            </v-card-title>
            <div v-if="tmpBoards.length==0">
                작성글이 없습니다.
            </div>
            <v-list v-else
                two-line
                class="review_list"
            >
                <div class="board_header">
                    <v-list-item>
                        <div class="board_name_header">
                            작성자
                        </div>
                        <div class="board_title_header">
                            제목
                        </div>
                        <div class="board_favorites_header">
                            <v-icon small color="rgb(128, 140, 247)">mdi-thumb-up</v-icon>
                        </div>
                        <div class="board_date_header">
                            작성일
                        </div>
                    </v-list-item>
                    <v-divider />
                </div>
                <div v-for="board, key in tmpBoards" :key="key" class="board_all">
                    <v-list-item :to="`/boards/${board.id}?user=${board.user}`">
                        <div class="board_name">
                            {{board.user}}
                        </div>
                        <div class="board_title">
                            {{board.title}}
                        </div>
                        <div class="board_favorites">
                            {{board.favorites}}
                        </div>
                        <div class="board_date">
                            {{board.updated_at}}
                        </div>
                        
                    </v-list-item>
                    <v-divider />
                </div>
            </v-list>
            <keep-alive>
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
            </keep-alive>
        </div>
    </v-card>
</template>
<script>
import {
    get_boards
} from '@/assets/board'
export default {
    props:{
        boards: Array,
        total: Number
    },
    data(){
        return {
            loading: false,
            start: 1,
            current: 1,
            length: 5,
            limit: Math.ceil(this.total/5),
            tmpBoards: this.boards,
            user_id: this.$route.params.id,
            view: 5
        }
    },
    computed:{
        pages: function () {
            return Array.from(
                { length: this.end - this.start +1},
                (e, i) => i + this.start
                
            );
        },
        end: function(){
            return Math.min(this.start + this.length -1, this.limit)
        },
        
    },
    watch:{
        total: function(newtotal){
            this.start = 1;
            this.current = 1;
            console.log(newtotal, this.view)
            this.limit = Math.ceil(newtotal / this.view);
            console.log(this.limit)
        },
        view: function (newview) {
            this.limit = Math.ceil(this.total / newview);
        },
    },
    methods:{
        async selectGym(gym) {
            this.$store.state.selected = false
            this.$store.state.selectedData = gym;
            this.$store.state.selected = true;
        },
        async handlePageClick(page) {
            if (this.current == page) return
            this.loading = true;
            this.current = page;
            const [success, res] = await get_boards((this.current-1)*this.length, this.length, this.user_id );
            if (!success) return
            this.tmpBoards = res.results
        },
        async handlePrevClick() {
            if (this.start == 1)  return;
            this.loading = true;
            const current = this.start - this.length;
            this.start = current;
            this.end = this.start + this.length -1
            this.current = current;
            const [success, res] = await get_boards((this.current-1)*this.length, this.length, this.user_id );
            if (!success) return
            this.tmpBoards = res.results
        },
        async handleNextClick() {
            if (this.end == this.limit) return;
            this.loading = true;
            const page = this.start + this.length;
            this.start = page;
            this.end = this.start + this.length -1
            this.current = page;
            const [success, res] = await get_boards((this.current-1)*this.length, this.length, this.user_id );
            if (!success) return
            this.tmpBoards = res.results
            
        },

    }
}
</script>
<style scoped>
.board_header {
    background-color: rgb(243, 243, 243);
}
.board_name_header {
    width: 80px;
    text-align: center;
}
.board_title_header {
    width: 50%;
    display:grid;
}
.board_favorites_header{
    width: 30%;
    padding: 0 10px 0 5px;
    font-size: 13px;
}
.board_date_header{
    width:15%;
}
.board_all {
    font-size: 14px;
}
.board_name {
    width: 80px;
    text-align: center;
}
.board_title {
    width: 50%;
    display:grid;
}
.board_favorites{
    width: 30%;
    padding: 0 10px 0 5px;
    font-size: 13px;
}
.board_date{
    width:15%;
}
</style>