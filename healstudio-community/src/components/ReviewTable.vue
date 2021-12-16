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
        </v-list>
    </v-card>
</template>
<script>
export default {
    setup() {
        
    },
    props:{
        metaData: Object,
        data: Array,
    },
    data(){
        return {
            listWidth: window.innerWidth - 602,
            listHeight: Math.round((window.innerHeight - 483) / 100) * 100,
        }
    },
    mounted(){
        console.log(this.reviews)
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