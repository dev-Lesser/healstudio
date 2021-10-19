<template>
    <div class="board_contents">
        
        <v-flex xs12 sm12 md8>
            <v-card-actions>
                <v-spacer/>
                작성자 : {{data.user}}
            </v-card-actions>
            <v-card-actions>
                <v-spacer/>
                작성일 : {{data.created_at}}
            </v-card-actions>
            <v-card outlined :min-height="150" class="d-flex flex-row align-center">
                {{data.contents}}
            </v-card>
            <v-layout style="display:flex; justify-content:center;">
                <v-flex xs12 sm8 md6>
                    <v-card-title>
                        좋아요/ 추천
                    </v-card-title>
                    <v-card outlined class="ma-3 pa-3">
                        <v-card-actions >
                            <div class="favorites_number_box">
                                {{data.favorites}}
                            </div>
                        <v-spacer />
                        <v-icon size=64 >mdi-heart</v-icon>
                        </v-card-actions>
                        <div class="mb-3">
                        지금 바로 게시물을 작성해 보세요
                        </div>
                        <v-btn block color="primary"><v-icon small class="mr-3">mdi-pencil</v-icon>작성하기</v-btn>
                    </v-card>
            </v-flex>
            </v-layout>
        </v-flex>
    </div>
</template>
<script>
export default {
    props: {
        data: Object
    },
}
</script>
<style scoped>
.board_contents{
    display: flex;
    justify-content: center;
}
.favorites_number_box{
    color:rgb(247, 137, 64);
    font-size: 36px;
}
</style>