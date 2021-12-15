<template>
  <v-app-bar
    app
    dark
    height="64"
  >
  <v-card-actions>
    <v-icon class="pl-3 mb-2" v-show="$route.name == 'Home'" @click="$store.state.selected = !$store.state.selected">mdi-format-align-justify</v-icon>
    <v-spacer />
    <v-btn outlined small @click="$router.push('/')">검색 홈</v-btn>
    <v-btn outlined small v-if=" token == null" @click="$router.push('/login')">로그인</v-btn>
    <v-btn outlined small v-else @click="logout">로그아웃</v-btn>
  </v-card-actions>
  </v-app-bar>
</template>
<script>
export default {
  data() {
    return {
      // token: window.localStorage.getItem(`token`),
      hasToken: null
    }
  },
  mounted(){
    console.log( window.localStorage.getItem("token"))
  },
  computed:{
    token(){
      return window.localStorage.getItem(`token`)
    }
  },
  watch:{
    token(){
      this.hasToken=this.token;
    }
  },
  methods:{
    async logout(){
      window.localStorage.setItem("token", null);
      // this.$router.push( {path:"/"} ).catch(error => {
      //         // self.loading = false;
      //     alert(error)
      //   })
      // this.token = null
    }
  }
}
</script>

