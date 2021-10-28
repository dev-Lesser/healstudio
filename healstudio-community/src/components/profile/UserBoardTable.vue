<template>
    <v-card class="pa-3 ma-3">
        
        <div>
            <v-card-title>
                최근 작성글
            </v-card-title>
            <div v-if="boards.length==0">
                작성글이 없습니다.
            </div>
            <v-list v-else
                two-line
                class="review_list"
            >
                <div class="review-header">
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
                <div v-for="board, key in boards" :key="key" class="board_all">
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
        </div>
    </v-card>
</template>
<script>

export default {
    props:{
        boards: Array
    },
    methods:{
        async selectGym(gym) {
            this.$store.state.selected = false
            this.$store.state.selectedData = gym;
            this.$store.state.selected = true;
        },

    }
}
</script>
<style scoped>
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