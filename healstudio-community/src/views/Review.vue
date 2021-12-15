<template>
<div class="reviews-card">
    <gym-detail :data="selectedData"/>
    <div style="display:flex">
    <div class="justify-center align-center d-flex">
    <v-card  class="ma-3 pa-3">
        <v-card-title>
            {{selectedData.name}}
            
        </v-card-title>
        <v-chip outlined class="box-hashtag-content ma-2" small v-for="keyword, i in selectedData.keywords" :key="`keyword--${i}`">#{{keyword}}</v-chip>
         <v-progress-linear
            indeterminate
            color="black"
            class="mt-12"
            v-if="loading"
            ></v-progress-linear>
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
        <div v-for="review, i in reviews" :key="i">
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
                    내용
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
    <v-spacer/>
    </div>
    </div>
</div>
</template>
<script>
import GymDetail from '@/components/GymDetail'
import { get_gym_by_id, get_reviews } from '@/assets/api'
    export default {
        components:{
            GymDetail
        },
        data() {
            return {
                info: null,
                rating: 5,
                desc: null,
                selectedRoadAddress: false,
                loading: false,
                reviews: null,
                listWidth: window.innerWidth - 602,
                listHeight: Math.round((window.innerHeight - 483) / 100) * 100,
            }
        },
        async mounted(){
            this.loading = true;
            if (this.$store.state.selectedData == null){  
                this.$store.state.selected = true;
                const [success, res] = await get_gym_by_id(this.$route.params.id);
                
                if (!success) this.status = -1;
                else {
                    this.$store.state.selectedData = res;
                    this.loading = false;
                }
            }
            await this.getReviews(this.$route.params.id, 0, 5)

        },
        computed: {
            selected() {
                return this.$store.state.selected;
            },
            selectedData() {
                return this.$store.state.selectedData;
            }
        },
        methods:{
            async getReviews(gymId, skip, limit){
                const [success, res] = await get_reviews(gymId, skip, limit);
                if (!success) this.status = -1;
                else {
                    this.reviews = res;
                    this.loading = false;
                }
            }
        },
    }
</script>
<style scoped>
.reviews-card{
    display: flex;
    font-family:'Jeju Gothic', sans-serif;

}
.review_list_item{
    font-size: 15px;
}
.review-header{
    font-size: 18px;
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