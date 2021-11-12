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
            <Pagination 
                @page-click="pageClick"
                :total="total"
                :current-num="1"
                :length="5"
                />
        </div>
    </v-card>
</template>
<script>
import {
    get_boards
} from '@/assets/board'
import Pagination from '@/components/Pagination'
export default {
    props:{
        boards: Array,
        total: Number
    },
    components:{
        Pagination
    },
    data(){
        return {
            loading: false,
            start: 1,
            current: 1,
            length: 5,
            tmpBoards: this.boards,
            user_id: this.$route.params.id,
        }
    },

    methods:{
        async pageClick(page) {
            this.page = page;
            const [success, res] = await get_boards((this.page-1)*this.length, this.length, this.user_id );
            if (!success) return
            this.tmpBoards = res.results
        },
        async selectGym(gym) {
            this.$store.state.selected = false
            this.$store.state.selectedData = gym;
            this.$store.state.selected = true;
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