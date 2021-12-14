<template>
  <v-app >
    <Header />
    
    <v-main>
      <side-nav-bar />
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import Header from './components/Header';
import SideNavBar from '@/components/SideNavBar'

export default {
  name: 'App',

  components: {
    Header,
    SideNavBar,
  },

  data: () => ({
    //
  }),
};
</script>
