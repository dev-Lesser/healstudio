<template>
    <v-layout wrap class="user_page_layout">
        
        <v-card height="700" width="200">
            asdfasd
        </v-card>
        <v-flex xs12 sm8 md8>
            <v-card height=500>
        <v-card-subtitle>
            아이디 : {{userDetails.user}}
        </v-card-subtitle>
        찜한목록 : {{userDetails.favList}}
        리뷰 : {{userDetails.reviews}}
        ip : {{userDetails.ip}}
         : {{userDetails.created_at}}
         : {{userDetails.last_login}}
        </v-card>
        </v-flex>
    </v-layout>
</template>
<script>
import {
    get_user_details
} from '@/assets/auth'
export default {
    data() {
        return {
            user_id: null,
            uuid : null,
            loading: false,
            status: 0
        }
    },
    async mounted(){
        this.user_id = window.localStorage.getItem("user_id")
        this.uuid = window.localStorage.getItem("token")
        if (this.user_id !== this.$route.params.id && this.uuid !== this.$route.query.uid) {
            alert('권한이 없습니다. 로그인을 해주세요.')
            this.$router.push('/login')

        }

        await this.getUserDetails()
    },
    methods:{
        async getUserDetails(){
            this.loading=true
            const [success, res] = await get_user_details(this.user_id, this.uuid);
            if (!success) this.status = -1;
            else {
                this.$store.state.userDetails = res
                this.loading = false;
            }
            console.log(this.$store.state.userDetails)
        }
    },
    computed:{
        userDetails(){
            return this.$store.state.userDetails
        }
    }
}
</script>
<style scoped>
.user_page_layout{
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>