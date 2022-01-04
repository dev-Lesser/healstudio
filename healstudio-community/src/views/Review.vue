<template>
<div class="reviews-card">
    <gym-detail :data="selectedData"/>
    
    <v-card class="reviews-container justify-center align-center d-flex">
        <v-container>
            <v-layout>
                <ad-box />
            </v-layout>
        <v-layout>
            <div class="justify-center align-center d-flex">
                <review-table :meta-data="selectedData" :data="reviews"/>
            </div>
        </v-layout>
        </v-container>
    </v-card>
</div>
</template>
<script>
import GymDetail from '@/components/GymDetail'
import AdBox from '@/components/AdBox'

import ReviewTable from '@/components/ReviewTable'
import { get_gym_by_id, get_reviews } from '@/assets/api'
    export default {
        components:{
            GymDetail,
            ReviewTable,
            AdBox
        },
        data() {
            return {
                info: null,
                rating: 5,
                desc: null,
                selectedRoadAddress: false,
                loading: false,
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
            },
            reviews(){
                return this.$store.state.reviews;
            }
        },
        methods:{
            async getReviews(gymId, skip, limit){
                const [success, res] = await get_reviews(gymId, skip, limit);
                if (!success) this.status = -1;
                else {
                    this.$store.state.reviews = res;
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
.reviews-container {
    width: calc(100vw - 350px);
}

</style>