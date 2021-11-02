<template>
    <div class="board_contents">
        
        <v-flex xs12 sm12 md12>
            
            <v-card :min-height="150" class="d-flex flex-row align-center ma-3 pa-3" flat>
                <div v-html=data.contents></div>
            </v-card>
            <v-divider/>
            <v-layout style="display:flex; justify-content:center;">
                <v-flex xs12 sm8 md6>
                    <v-card-title>
                        좋아요/ 추천
                    </v-card-title>
                    <v-card outlined class="ma-3 pa-9">
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
                        <v-btn block color="primary" @click="handlePost"><v-icon small class="mr-3">mdi-pencil</v-icon>작성하기</v-btn>
                    </v-card>
            </v-flex>
            </v-layout>
        </v-flex>
    </div>
</template>
<script>
export default {
    props: {
        data: Object,
        
    },
    data(){
        return {
            user_id: window.localStorage.getItem('user_id'),
            uuid: window.localStorage.getItem('token')
        }
    },
    methods:{
        async handlePost(){
            if (!this.user_id && !this.uuid){
                alert('로그인이 필요한 서비스입니다')
                this.$router.push('/login')
            }
            else this.$router.push('/board/post')
        }
    }
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