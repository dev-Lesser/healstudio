<template>
    <v-layout wrap class="user_page_layout" v-if="userMeta!=null&&userDetails!=null&&userBoards!=null">
        
        <v-card  class="ma-3 pa-3" flat>
            <v-avatar  color="indigo" size="200">
                <v-icon dark size="90">
                    mdi-account-circle
                </v-icon>
            </v-avatar>
                    
            <div class="user_profile_bar">
                {{userMeta.user}}
            </div>
            <v-list
                two-line
                class="review_list"
            >
            <v-list-item>
                <v-list-item-content>
                    <a href="#user_favorite" class="user_profile_favorite" >
                        찜한목록 (5개)
                    </a>
                </v-list-item-content>
            </v-list-item>
            <v-divider />
            <v-list-item>
                <v-list-item-content>
                    <a href="#user_reviews" class="user_profile_review">
                        작성 리뷰
                    </a>
                </v-list-item-content>
            </v-list-item>
            <v-divider />
            <v-list-item>
                <v-list-item-content>
                    <a href="#user_reviews" class="user_profile_review">
                        작성글
                    </a>
                </v-list-item-content>
            </v-list-item>
            <v-divider />
            </v-list>
        </v-card>
        <v-flex xs12 sm12 md8>
            <v-flex xs12 md12>
                <user-meta :user-meta="userMeta" :favGymLength="favCount" :reviewsLength="reviewCount" :boardsLength="boardCount"/>
            </v-flex>
            <v-flex xs12 sm12 md12>
                <user-favorite-table  id="user_favorite" :favGym="userDetails" />
            </v-flex>
            <v-flex xs12 sm12 md12>
                <user-board-table  id="user_favorite" :boards="userBoards" :total="boardCount"/>
            </v-flex>
            <v-flex xs12 sm12 md12>
                <user-reviews-table id="user_reviews" :data="userReviews" />
            </v-flex>
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
import {
    get_boards
} from '@/assets/board'
import UserMeta from '@/components/profile/UserMeta'
import UserFavoriteTable from '@/components/profile/UserFavoriteTable'
import UserBoardTable from '@/components/profile/UserBoardTable'
import UserReviewsTable from '@/components/profile/UserReviewsTable'
export default {
    components:{
        UserMeta,
        UserFavoriteTable,
        UserBoardTable,
        UserReviewsTable
    },
    data() {
        return {
            user_id: null,
            uuid : null,
            loading: false,
            status: 0,
            favCount: 0,
            reviewCount: 0,
            boardCount: 0,
        }
    },
    async mounted(){
        this.user_id = window.localStorage.getItem("user_id")
        this.uuid = window.localStorage.getItem("token")
        
        if (this.user_id !== this.$route.params.id && this.uuid !== this.$route.query.uid) {
            alert('권한이 없습니다. 로그인을 해주세요.')
            this.$router.back()
        }

        await this.getUserDetails()
        await this.getAllReviews()
        await this.getAllBoards()
    },
    methods:{
        async getUserDetails(){
            this.loading=true
            const [success, res] = await get_user_details(this.user_id, this.uuid);
            if (!success) this.status = -1;
            else {
                this.$store.state.userDetails = res.results
                this.$store.state.userMeta = res.user // 하나만 meta 정보 보여주기 위함 > 리뷰가 없을때 활동이 없을때 에러가 남
                this.favCount = res.fav_count
                this.loading = false;
            }
        },
        async getAllReviews(){
            this.loading = true;
            const [skip, limit]= [0, 5];
            const [success, res] = await get_reviews('all', skip, limit, this.user_id)

            success;
            this.$store.state.userReviews = res.results;
            this.reviewCount = res.review_count
        },
        async getAllBoards(){
            this.loading = true;
            const [skip, limit]= [0, 5];
            const [success, res] = await get_boards(skip, limit, this.user_id )
            success;
            this.$store.state.userBoards = res.results;
            this.boardCount = res.board_count
        }
    },
    computed:{
        userDetails(){
            return this.$store.state.userDetails;
        },
        userReviews(){
            return this.$store.state.userReviews;
        },
        userBoards(){
            return this.$store.state.userBoards;
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
    font-family:'Jeju Gothic', sans-serif;
}
.user_profile_bar{
    margin-top: 30px;
    font-size: 20px;
    line-height: 24px;
    color: var(--color-fg-muted);
}
.user_profile_favorite{
    color: black;
    text-decoration: none;
}
.user_profile_favorite:after{
    background: none repeat scroll 0 0 transparent;
    bottom: 0;
    content: "";
    display: block;
    height: 2px;
    left: 50%;
    position: absolute;
    background: #FFC0FF;
    transition: width 0.3s ease 0s, left 0.3s ease 0s;
    width: 0;

}
.user_profile_review:hover:after { 
  width: 100%; 
  left: 0; 
}

.user_profile_review{
    color: black;
    text-decoration: none;
}
.user_profile_review:after{
    background: none repeat scroll 0 0 transparent;
    bottom: 0;
    content: "";
    display: block;
    height: 2px;
    left: 50%;
    position: absolute;
    background: #FFC0FF;
    transition: width 0.3s ease 0s, left 0.3s ease 0s;
    width: 0;

}
.user_profile_favorite:hover:after { 
  width: 100%; 
  left: 0; 
}


</style>