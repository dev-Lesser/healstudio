<template>
  <v-app-bar
    app
    dark
    height="64"
    class="header"
  >
    <v-icon class="mr-5" v-show="$route.name == 'Home'" @click="$store.state.selected = !$store.state.selected">mdi-format-align-justify</v-icon>
    <v-btn outlined class="mr-5" small v-if="user_id=='null'" @click="$router.push('/login')">로그인</v-btn>
    <v-btn outlined class="mr-5" small v-else @click="logout">로그아웃</v-btn>
    <div class="header_hello_user" v-if="user_id">
      {{helloText}}
    </div>
    <v-spacer />
    <v-btn outlined small @click="$router.push('/')">검색 홈</v-btn>
    
    
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
    console.log(window.localStorage.getItem(`user_id`))
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
      if (this.user_id!='null'){
        console.log('로그인됨')
        this.helloText = `반갑습니다 ${this.user_id} 님!`
      }
    },
    async logout(){
      window.localStorage.setItem("token", null);
      window.localStorage.setItem("user_id", null);
      this.$router.go()
      // this.$router.push( {path:"/"} ).catch(error => {
      //         // self.loading = false;
      //     alert(error)
      //   })
      // this.token = null
    }
  }
}
</script>
<style scoped>
.header_hello_user{
  font-family:'Jeju Gothic', sans-serif;
}
</style>