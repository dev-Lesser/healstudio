<template>
<v-flex xs12 sm12 md12 v-if="metaData!=null">
    <v-card  class="ma-3 pa-3" >
        <v-card-title>
            {{metaData.name}}
        </v-card-title>
        <v-divider />
        <v-chip outlined class="box-hashtag-content ma-2" small v-for="keyword, i in metaData.keywords" :key="`keyword--${i}`">#{{keyword}}</v-chip>
        
        <v-list
            two-line
            class="review_list"
            v-if="data!=null&&data.length>0"
            height="410"
            :key="rerender"
        >
            <div class="review-header">
                <v-list-item>
                    <div class="review-user">
                        작성자
                    </div>
                    <div class="review-rating">
                        별점
                    </div>
                    <div class="review-content">
                        내용
                    </div>
                    <div class="review-created">
                        작성일/수정일
                    </div>
        
                    
                </v-list-item>
                <v-divider />
            </div>
            <div v-for="review, i in data" :key="i">
                <v-list-item :key="review.id" class="review_list_item">
                    <div class="review-user">
                        <v-avatar class="mr-3" color="indigo" size="36">
                            <v-icon dark>
                                mdi-account-circle
                            </v-icon>
                        </v-avatar>
                        
                        <div>
                        {{review.user}}
                        </div>
                    </div>
                    <div class="review-rating">
                    <v-rating
                        v-model="review.point"
                        background-color="grey"
                        color="yellow accent-4"
                        dense
                        hover
                        length="5"
                        half-increments
                        size="18"
                        readonly
                        ></v-rating>
                    </div>
                    <div class="review-content">
                    {{review.contents}}
                    <div v-if="user_id==review.user">
                        <v-icon 
                            small
                            class="mr-2"
                            color="rgb(116, 116, 216)"
                            @click="openEditReview(review)"
                        >
                            mdi-pencil
                        </v-icon>
                        <v-icon
                            small
                            color="rgb(216, 116, 116)"
                            @click="openDeleteReview(review)"
                        >mdi-delete</v-icon>
                    </div>
                    </div>
                    
                    <div class="review-created">
                    {{review.created_at >= review.updated_at ? review.created_at.split(" ")[0] : review.updated_at.split(" ")[0]}}
                    </div>
                    
                </v-list-item>
                <v-divider />
            </div>
        </v-list>
        
        <v-list
            two-line
            :width="listWidth"
            class="review_list"
            style="display:flex; align-items: center; justify-content: center;"
            v-else
        >
            <no-data />
        </v-list>
        <!-- 페이지네이션 -->
        <Pagination 
            @page-click="pageClick"
            :total="total"
            :length="5"
            :current-num="1"
            />
        <v-progress-linear
            indeterminate
            color="black"
            class="mt-12"
            v-if="loading"
            height="3"
            rounded
            ></v-progress-linear>
        <v-progress-linear
            color="black"
            class="mt-3 mb-2"
            rounded
            height="3"
            v-else
        ></v-progress-linear>

        <div style="display:flex; align-items:center;">
            <v-btn 
            @click="openCreateReview" 
            block 
            color="primary"
            height="40"
            >
                <v-icon class="mr-2" small >mdi-pencil</v-icon>
                리뷰 작성하기
            </v-btn>
        </div>
        <contents-form :overlay="overlay" :updateId="updateId" :meta-data="metaData" :point="point" :contents="contents" :isUpdateClick="isUpdateClick"/>
        
        
        <v-overlay :value="delete_overlay" light  >
            <v-card class="ma-3 pa-3" :width="500"
            light>
            <v-card-title>
                정말로 삭제 하시겠습니까?
            </v-card-title>
            <v-divider />
            <v-card-subtitle>
            별점 <v-rating
            v-model="point"
            :value="contents"
            background-color="grey"
            length="5"
            read-only
            color="yellow accent-4"
            dense
            half-increments
            size="15"
            ></v-rating> 
            내용
            <v-card-subtitle>
                {{contents}}
            </v-card-subtitle>
            </v-card-subtitle>
            <v-divider />
            <v-card-actions>
                <v-btn color="error" @click="deleteReview">삭제하기</v-btn>
                <v-spacer />
                <v-btn color="primary" @click="closeReview"> 취소 </v-btn>
            </v-card-actions>
            </v-card>
            
        </v-overlay>
    </v-card>
</v-flex>
</template>
<script>
import ContentsForm from '@/components/ContentsForm'
import NoData from '@/components/NoData'
import Pagination from '@/components/Pagination'
import {
    delete_review,
    get_reviews ,
} from '@/assets/api'

export default {
    components: {
        ContentsForm,
        NoData,
        Pagination,
    },
    props:{
        metaData: Object,
        data: Array,
        total: Number
    },
    data(){
        return {
            listWidth: window.innerWidth - 600,
            listHeight: Math.round((window.innerHeight - 483) / 100) * 100,
            isShown: true,
            point: 5,
            contents: '',
            pages: 5,
            end: 100,
            loading: false,
            isUpdateClick: false,
            updateId: null,
            delete_overlay: false,
            user_id: window.localStorage.getItem(`user_id`),
            uuid: window.localStorage.getItem(`token`),
            start: 1,
            current: 1,
            length: 5,
            limit: 30,
            rerender: 0,
            // total: null,
        }
    },
    async created(){
        await this.init();
    },
    methods:{
        async init(){
            this.$store.state.overlay = false
            this.contents = ''
            this.point = 5
            this.isUpdateClick = false
            this.delete_overlay = false
        },
        async closeReview(){
            await this.init();
        },

        openCreateReview(){
            if (!window.localStorage.getItem("user_id")) {
                alert('로그인이 필요한 서비스 입니다')
                this.$router.push('/login');
            }
            else (this.$store.state.overlay = true)
        },
        openEditReview(item){            
            if (!window.localStorage.getItem("user_id")) {
                alert('로그인이 필요한 서비스 입니다')
                this.$router.push('/login');
                return
            }
            this.updateId = item.id
            this.isUpdateClick = true
            this.contents = item.contents
            this.point = item.point
            this.$store.state.overlay = true; // 창을 펼친다
        },
        openDeleteReview(item){
            if (!window.localStorage.getItem("user_id")) {
                alert('로그인이 필요한 서비스 입니다')
                this.$router.push('/login');
                return
            }
            this.updateId = item.id
            this.isUpdateClick = true
            this.contents = item.contents
            this.point = item.point
            this.delete_overlay = true; // 창을 펼친다
        },
        
        async deleteReview(){
            const [success, res] = await delete_review(
                this.updateId,
                this.$route.params.id,
                this.user_id
                );
            if (!success) {
                this.status = -1;
                alert(res)
            }
            else {
                await this.init();
                this.rerender +=1;
            }
            
            this.loading = false;
        },
        async pageClick(page){
            this.page = page
            await this.getReviews(this.$route.params.id, (this.page-1)*this.length, this.length)
        },
        async getReviews(gymId, skip, limit){
            const [success, res] = await get_reviews(gymId, skip, limit, null);
            if (!success) this.status = -1;
            else {
                this.$store.state.reviews = res.results;
                this.total = res.review_count;
                this.loading = false;
            }
        },
    },

    async beforeUnmount(){
        await this.init();
    },
    computed:{
        overlay: {
            set: function(){
                // re
            },
            get: function(){
                return this.$store.state.overlay;
            }
        }
    }

    
}
</script>
<style scoped>
.review_list_item{
    font-size: 13px;
}
.review-header{
    font-size: 15px;
}
.review-user {
    display: flex;
    justify-content: left;
    align-items: center;
    width: 100px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;  /* 말줄임 적용 */;
}
.review-rating {
    width: 160px;
    text-align: center;
}
.review-content {
    width: 75%;
    display:grid;
}
.review-created{
    width: 15%;
}


</style>