<template>
    <v-card class="ma-3 pa-3">
        <!-- {{data}} -->
        <div v-if="data.length==0">
            작성 리뷰가 없습니다
        </div>
        <div v-else>
            <v-card-title>
                작성리뷰
            </v-card-title>
            <v-list
                two-line
                class="review_list"
                height="410"
            >
                <div class="review-header">
                    <v-list-item>
                        <div class="review_gym_img_header">

                        </div>
                        <div class="review_gym_name_header">
                            헬스장
                        </div>
                        <div class="review_user_header">
                            작성자
                        </div>
                        <div class="review_rate_header">
                            평점
                        </div>
                        <div class="review_contents_header">
                            작성글
                        </div>
                        <div class="review_date_header">
                            작성일/수정일
                        </div>
                    </v-list-item>
                    <v-divider />
                </div>
                <div v-for="review, key in data" :key="key" class="favorite_gym_contents">
                    <v-list-item >
                        <div class="review_gym_img">
                            <v-img width="50" height="50" :src="review.gymInfo.imageUrl"></v-img>
                        </div>
                        <div class="review_gym_name">
                            
                            <div>{{review.gymInfo.name}}</div>
                        </div>
                        <div class="review_user">
                            {{review.user}}
                        </div>
                        <div class="review_rate">
                            <v-rating
                            v-model="review.point"
                            :value="review.point"
                            background-color="grey"
                            length="5"
                            read-only
                            color="yellow accent-4"
                            dense
                            half-increments
                            size="15"
                            ></v-rating> 
                        </div>
                        <div class="review_contents">
                            {{review.contents}}
                        </div>
                        <div class="review_date">
                            {{review.updated_at}}
                        </div>
                    </v-list-item>
                    <v-divider />
                </div>
            </v-list>
        </div>
    </v-card>
</template>
<script>
export default {
    props: {
        data: Array,
    },
}
</script>
<style scoped>
.review_gym_img_header{
    width: 80px;
    /* font-size: 15px; */
}
.review_gym_img{
    width: 80px;
    /* font-size: 15px; */
}
.review_gym_name_header{
    width: 200px;
}
.review_gym_name{
    display: grid;
    width: 200px;
    font-size: 15px;
}
.review_user_header{
    width: 100px;
    /* font-size: 15px; */
}
.review_user{
    width: 100px;
    font-size: 15px;
}
.review_rate_header{
    width: 150px;
}
.review_rate{
    width: 150px;
}
.review_contents_header{
    width: 20%;
}
.review_contents{
    width: 20%;
    font-size: 12px;

}
.review_date_header{
    width: 15%;
}
.review_date{
    width: 15%;
    font-size: 12px;
}
</style>