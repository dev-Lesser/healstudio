<template>
    <v-card  class="ma-3 pa-3">
        <v-card-title>
            {{metaData.name}}
            
        </v-card-title>
        <v-chip outlined class="box-hashtag-content ma-2" small v-for="keyword, i in metaData.keywords" :key="`keyword--${i}`">#{{keyword}}</v-chip>
        <v-list
            two-line
            :width="listWidth"
            :height="listHeight"
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
                <div class="review-updated">
                    수정일
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
                {{review.created_at}}
                </div>
                <div class="review-updated">
                {{review.updated_at}}
                </div>
                
            </v-list-item>

        </div>
        <v-divider />
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
                    <v-btn @click="overlay = !overlay">취소</v-btn>
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
</template>
<script>
import NoData from '@/components/NoData'
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
            listWidth: window.innerWidth - 602,
            listHeight: Math.round((window.innerHeight - 483) / 100) * 100,
            isShown: true,
            overlay: false,
            point: 0,
            contents: '',
        }
    },
    methods:{
        async createReview(){
            console.log(this.point,this.contents)
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
    width: 15%;
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
</style>