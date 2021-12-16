<template>
  <v-app app >
    <Header />
    <v-main>
      <vue-page-transition name="fade">
        <div class="entire-outbox">
          
        <router-view/>
        </div>
      </vue-page-transition>
    </v-main>
  </v-app>
</template>

<script>
import Header from './components/Header';

export default {
  name: 'App',

  components: {
    Header,
  },

  data: () => ({
    //
  }),
};
</script>
<style scoped>
.entire-outboxt {
  width: 500px;
}
</style>