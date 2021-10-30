<template>
    <v-card class="pa-3 ma-3">
        <div v-if="favGym.length==0">
            찜한 헬스장이 없습니다
        </div>
        <div v-else>
            <v-card-title>
                찜한 목록 (5개)
            </v-card-title>
            <v-list
                two-line
                class="review_list"
            >
                <div class="review-header">
                    <v-list-item>
                        <div class="favorite_gym_img">
                            
                        </div>
                        <div class="favorite_gym_name">
                            Where?
                        </div>
                        <div class="favorite_gym_address">
                            주소
                        </div>
                        <div class="favorite_gym_heart">
                            <v-icon class="image-region-tag" small >mdi-heart</v-icon>
                        </div>
                    </v-list-item>
                    <v-divider />
                </div>
                <div v-for="gym, key in favGym" :key="key" class="favorite_gym_contents">
                    <v-list-item :to="`/review/${gym.gymInfo.id}`" @click="selectGym(gym.gymInfo)">
                        <div class="favorite_gym_img">
                            <v-img width="50" height="50" :src="gym.gymInfo.imageUrl"></v-img>
                        </div>
                        <div class="favorite_gym_name">
                            {{gym.gymInfo.name}}
                        </div>
                        <div class="favorite_gym_address">
                            {{gym.gymInfo.fullAddress}}
                        </div>
                        <div class="favorite_gym_heart">
                            <v-icon class="image-region-tag" small color="rgb(255, 116, 116)" @click="handleFavorite">mdi-heart</v-icon>
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
    props:{
        favGym: Array
    },
    methods:{
        handleFavorite(e){
            console.log(e)
        },
        async selectGym(gym) {
            this.$store.state.selected = false
            this.$store.state.selectedData = gym;
            console.log(gym)
            this.$store.state.selected = true;
        },
    }
}
</script>
<style scoped>
.favorite_gym_img {
    width: 80px;
    text-align: center;
}
.favorite_gym_name {
    width: 30%;
    display:grid;
}
.favorite_gym_address{
    width: 50%;
    padding: 0 10px 0 5px;
    font-size: 13px;
}
.favorite_gym_heart{
    width:5%;
}
</style>