<template>
    <div>
        {{$route.params}}
        {{$route.query}}
    </div>
</template>
<script>
export default {
    data() {
        return {
            user_id: null,
            uuid : null
        }
    },
    async mounted(){
        this.user_id = window.localStorage.getItem("user_id")
        this.uuid = window.localStorage.getItem("token")
        console.log(this.user_id)
        if (this.user_id !== this.$route.params.id && this.uuid !== this.$route.params) {
            alert('권한이 없습니다. 로그인을 해주세요.')
            this.$router.push('/login')

        }
    }
}
</script>