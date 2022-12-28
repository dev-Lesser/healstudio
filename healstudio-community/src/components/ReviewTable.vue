<template>
<v-flex xs12 sm12 md12 >
    <v-card  class="ma-3 pa-3" height="600">
        <v-card-title>
            {{metaData.name}}
        </v-card-title>
        <v-chip outlined class="box-hashtag-content ma-2" small v-for="keyword, i in metaData.keywords" :key="`keyword--${i}`">#{{keyword}}</v-chip>
        
        <v-list
            two-line
            class="review_list"
            v-if="data.length>0"
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
                    작성일
                </div>
                <div class="review-action">
                    수정/삭제
                </div>
            </v-list-item>
        </div>
        <div v-for="review, i in data" :key="i">
            <v-divider />
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
                    background-color="white"
                    color="yellow accent-4"
                    dense
                    half-increments
                    size="18"
                    readonly
                    ></v-rating>
                </div>
                <div class="review-content">
                {{review.contents}}
                </div>
                <div class="review-created">
                {{review.created_at >= review.updated_at ? review.created_at.split(" ")[0] : review.updated_at.split(" ")[0]}}
                </div>
                <div>
                    <v-icon
                        small
                        class="mr-2"
                        color="rgb(116, 116, 216)"
                        @click="overlay = !overlay"
                    >
                        mdi-pencil
                    </v-icon>
                    <v-icon
                        small
                        color="rgb(216, 116, 116)"
                        @click="deleteReview(review)"
                    >
                        mdi-delete
                    </v-icon>
                </div>
            </v-list-item>
        </div>
        <v-divider />
        <v-progress-linear
            indeterminate
            color="black"
            class="mt-12"
            v-if="loading"
            ></v-progress-linear>
            <v-progress-linear
            color="black"
            class="mt-3 mb-2"
            v-else
            ></v-progress-linear>
            <!-- <div class="d-flex flex-row justify-center">
                <v-icon class="pagination_page" @click="handlePrevClick" :color="start == 1 ? '#adadad' : '#757575'">mdi-chevron-left</v-icon>
                <div class="pagination_page d-flex flex-row justify-center align-center" 
                v-for="p in pages" :key="p" 
                :class="{ selected_page: current == p }" 
                @click="handlePageClick(p)">
                    {{ p }}
                </div>
                <v-icon class="pagination_page" @click="handleNextClick" :color="end == limit ? '#adadad' : '#757575'">mdi-chevron-right</v-icon>
            </div> -->
        <v-btn @click="overlay = !overlay"> <v-icon class="mr-2" small >mdi-pencil</v-icon>리뷰 작성하기</v-btn>
        <v-overlay :value="overlay" light  >
            <v-card class="ma-3 pa-3" :width="500"
            :height="400" light>
                <v-card-title>
                    리뷰
                    <v-card-actions>
                        <div><v-chip outlined>{{metaData.name}}</v-chip></div>
                    </v-card-actions>
                </v-card-title>
                <v-divider />
                    
                    <v-card-actions>
                        <div>
                            평점 : 
                        </div>
                        <v-rating
                            v-model="point"
                            background-color="grey"
                            hover
                            length="5"
                            color="yellow accent-4"
                            dense
                            half-increments
                            size="25"
                            ></v-rating> 
                        <v-spacer />
                        <div>{{point}} 점</div>
                    </v-card-actions>
                    
                
                
                
                <v-divider class="mt-6" />
                <v-textarea
                v-model="contents"
                clearable	
                outlined
                dense
                class="ma-1 pa-2"
                label="한줄평 50자"
                height=100
                color="grey"
                ></v-textarea>
                <v-card-actions>
                    <v-btn @click="createReview">작성하기</v-btn>
                    <v-spacer/>
                    <v-btn @click="init">취소</v-btn>
                </v-card-actions>
            </v-card>
        </v-overlay>
        </v-list>
        
        <v-list
            two-line
            :width="listWidth"
            :height="listHeight"
            class="review_list"
            v-else
        >
        <no-data />
        </v-list>
    </v-card>
</v-flex>
</template>
<script>
import NoData from '@/components/NoData'
import {create_review, update_review} from '@/assets/api'
export default {
    components: {
        NoData
    },
    props:{
        metaData: Object,
        data: Array,
    },
    data(){
        return {
            listWidth: window.innerWidth - 600,
            listHeight: Math.round((window.innerHeight - 483) / 100) * 100,
            isShown: true,
            overlay: false,
            point: 0,
            contents: '',
            pages: 5,
            start:1,
            end: 100,
            current: 1,
            loading: false,
        }
    },
    methods:{
        async init(){
            this.overlay = false
            this.contents = ''
            this.point = 0
        },
        async createReview(){
            const [success, res] = await create_review(
                this.$route.params.id,
                "test",
                this.contents,
                this.point
                );
                if (!success) {
                    this.status = -1;
                    alert(res)
                }
                else {
                    await this.init();
                }
                this.loading = false;
        },
        async editReview(item){
            const [success, res] = await update_review(
                item.id,
                this.$route.params.id,
                "test",
                item.contents,
                item.point
                );
                if (!success) {
                    this.status = -1;
                    alert(res)
                }
                else {
                    await this.init();
                }
                this.loading = false;
        },
        async deleteReview(item){
            console.log('delete', item)
        }
    },

    mounted(){

    },

    
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
    width: 10%;
}
.review-rating {
    width: 130px;
    text-align: center;
}
.review-content {
    width: 45%;
}
.review-created{
    width: 15%;
}
.review-updated{
    width: 15%;
}

.pagination_page {
        cursor: pointer;
        width: 34px;
        height: 34px;
        border-radius: 17px;
        text-align: center;
        margin: 4px;
    }
</style>