<template>
  <v-app-bar
    app
    dark
    height="64"
    class="header"
  >
    <v-icon class="mr-5" v-show="$route.name == 'Home'" @click="$store.state.selected = !$store.state.selected">mdi-format-align-justify</v-icon>
    <v-btn outlined  class="mr-5" @click="$router.push('/')">검색 홈</v-btn>
    <v-btn outlined  @click="$router.push('/boards')">자유게시판</v-btn>
    <v-spacer />
    
    <div class="header_hello_user" v-if="user_id">
      {{helloText}}
    </div>
    
    <v-btn outlined class="ml-5 mr-3" v-if="user_id==null" @click="$router.push('/login')">로그인</v-btn>
    <v-btn outlined class="ml-5 mr-3" v-else @click="logout">로그아웃</v-btn>
    <v-btn  @click="gotoUserPage" v-if="user_id!=null" light>My Page</v-btn>
    
    
  </v-app-bar>
</template>
<script>
export default {
  data() {
    return {
      hasToken: null,
      helloText: null,
      user_id: window.localStorage.getItem(`user_id`)
    }
  },
  async created(){
    await this.isLogin();
    
  },
  async updated(){
    await this.isLogin();
  },
  computed:{
    token(){
      return window.localStorage.getItem(`token`)
    },
    user(){
      return window.localStorage.getItem(`user_id`)
    }
  },
  watch:{
    token(){
      this.hasToken=this.token;
    }
  },
  methods:{
    async isLogin(){
      this.user_id = window.localStorage.getItem("user_id")
      if (this.user_id!=null){
        this.helloText = `반갑습니다 ${this.user_id} 님!`
      }
    },
    async logout(){
      window.localStorage.removeItem("token");
      window.localStorage.removeItem("user_id");
      this.$router.go()

    },
    async gotoUserPage(){
      const uuid = window.localStorage.getItem(`token`)
      this.$router.push(`/user/${this.user_id}?uid=${uuid}`)
    }
  }
}
</script>
<style scoped>
.header{
  font-family:'Jeju Gothic', sans-serif;
}
.header_hello_user{
  font-family:'Jeju Gothic', sans-serif;
}
</style>