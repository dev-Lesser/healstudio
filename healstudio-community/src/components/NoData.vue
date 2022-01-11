<template>
    <div class="no_data_box">
        <div class="no_data_box_contents">
        등록된 {{ this.content }}가 없습니다
        </div>
        <div class="create_btn">
            지금 바로 작성하기
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            content : ''
        }        
    },
    mounted(){
        console.log(this.$route.name)
        if (this.$route.name == "Trainer") this.content = "트레이너 리뷰"
        else if (this.$route.name == "Review") this.content = "헬스장 리뷰"
        
    }
}
</script>