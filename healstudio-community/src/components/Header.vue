<template>
  <v-app-bar
    app
    dark
    height="64"
  >
  <v-card-actions>
    <v-spacer />
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

