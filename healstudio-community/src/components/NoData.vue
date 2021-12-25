<template>
    <div class="no_data_box">
        <v-img :src="nodata_img" height="100" width="100"></v-img>
        <br />
        <div class="no_data_box_contents">
        등록된 {{ this.content }}가 없습니다
        </div>
        
        
    </div>
</template>
<script>
import {
    create_review, 
} from '@/assets/api'

import nodata_img from '@/assets/nodata.png'
export default {
    data() {
        return {
            content : '',
            nodata_img: nodata_img
        }        
    },
    mounted(){
        console.log(this.$route.name)
        if (this.$route.name == "Trainer") this.content = "트레이너 리뷰"
        else if (this.$route.name == "Review") this.content = "헬스장 리뷰"
        
    },
    methods:{
        async createReview(){
            if (this.contents.length > 50){
                alert("리뷰 길이가 50을 넘었습니다.")
                return
            }
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
                    this.$router.go()
                }
                this.loading = false;
        },
    }
}
</script>
<style scoped>
.no_data_box{

}
</style>