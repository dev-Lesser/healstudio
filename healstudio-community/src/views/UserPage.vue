<template>
    <v-layout wrap class="user_page_layout">
        
        <v-card  class="ma-3 pa-3" flat>
            <v-avatar  color="indigo" size="200">
                <v-icon dark>
                    mdi-account-circle
                </v-icon>
            </v-avatar>
                    
            <div class="user_profile_bar">
                {{userMeta.user}}
            </div>
            <div class="user_profile_edit">
                <v-btn> Edit profile </v-btn>
            </div>
            <v-list
                two-line
                class="review_list"
            >
            <v-list-item>
            <div class="user_profile_favorite">
                찜한목록
            </div>
            </v-list-item>
            <v-list-item>
            <div class="user_profile_review">
                나의 리뷰
            </div>
            </v-list-item>
            </v-list>
        </v-card>
        <v-flex xs12 sm8 md8>
            <v-card>
                <v-card-subtitle>
                    아이디 : {{userMeta.user}}
                </v-card-subtitle>
                <v-card-subtitle>
                    찜한 헬스장 개수 : {{userDetails.length}}
                </v-card-subtitle>
                <v-card-subtitle>
                    내가 쓴 리뷰 개수 : {{userReviews.length}}
                </v-card-subtitle>
                ip : {{userMeta.ip}}
                회원가입: {{userMeta.created_at}}
                최근로그인: {{userMeta.last_login}}
            </v-card>
        </v-flex>
    </v-layout>
</template>
<script>
import {
    get_reviews
} from '@/assets/api'
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
        await this.getAllReviews()
    },
    methods:{
        async getUserDetails(){
            this.loading=true
            const [success, res] = await get_user_details(this.user_id, this.uuid);
            if (!success) this.status = -1;
            else {
                this.$store.state.userDetails = res
                console.log(res)
                this.$store.state.userMeta = res[0] // 하나만 meta 정보 보여주기 위함
                this.loading = false;
            }
        },
        async getAllReviews(){
            this.loading = true;
            const [skip, limit]= [0, 5];
            const [success, res] = await get_reviews('all', skip, limit, this.user_id)
            console.log(success)
            this.$store.state.userReviews = res;
        }
    },
    computed:{
        userDetails(){
            return this.$store.state.userDetails;
        },
        userReviews(){
            return this.$store.state.userReviews;
        },
        userMeta(){
            return this.$store.state.userMeta;
        }
    }
}
</script>
<style scoped>
.user_page_layout{
    display: flex;
    justify-content: center;
    /* align-items: center; */
}
.user_profile_bar{
    
    font-size: 20px;
    font-style: normal;
    font-weight: 300;
    line-height: 24px;
    color: var(--color-fg-muted);
}
</style>