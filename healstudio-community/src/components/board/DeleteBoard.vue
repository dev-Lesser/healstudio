<template>
    <v-overlay light  >
            <v-card class="ma-3 pa-3" :width="500"
            light>
            <v-card-title>
                정말로 삭제 하시겠습니까?
            </v-card-title>
            <v-divider />
        
            <v-card-actions>
                <v-btn color="error" @click="deleteReview">삭제하기</v-btn>
                <v-spacer />
                <v-btn color="primary" @click="closeReview"> 취소 </v-btn>
            </v-card-actions>
            </v-card>
            
        </v-overlay>
</template>
<script>
import { delete_board} from '@/assets/board'
export default {
    props: {
        metaContents: Object,
    },
    data(){
        return {
            user_id: window.localStorage.getItem('user_id'),
            uuid: window.localStorage.getItem('token')
        }
    },
    methods:{
        async deleteReview(){
            const success = await delete_board(this.user_id, this.uuid, this.metaContents.id, this.metaContents.title)
            if (success) {
                this.$store.state.boardDeleteOveray = false
                this.$router.push('/boards')
            }
        },
        async closeReview(){
            this.$store.state.boardDeleteOveray=false;
        }
    },
}
</script>