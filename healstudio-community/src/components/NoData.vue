<template>
    <div class="no_data_box" >
        <v-img :src="nodata_img" height="100" width="100"></v-img>
        <br />
        <div class="no_data_box_contents">
        등록된 {{ this.content }}가 없습니다
        </div>
        
        
    </div>
</template>
<script>

import nodata_img from '@/assets/nodata.png'
export default {
    data() {
        return {
            content : '',
            nodata_img: nodata_img
        }        
    },
    mounted(){
        if (this.$route.name == "Trainer") this.content = "트레이너 리뷰"
        else if (this.$route.name == "Review") this.content = "헬스장 리뷰"
        
    },
    methods:{
        
    }
}
</script>
<style scoped>
.no_data_box{
    height: 434px;
    display: flex;
    align-items: center;
}
</style>