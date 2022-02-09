<template>
  <v-app app >
    <Header />
    <v-main >
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
import {get_meta} from '@/assets/api'
import axios from 'axios'
export default {
  name: 'App',

  components: {
    Header,
  },

  data: () => ({
    //
  }),
  async created(){
    if (this.$store.state.meta == null) await this.getMeta();
  },
  methods:{
    async getMeta(){
      const [success, res] = await get_meta()
      success;
      this.$store.state.meta = res;
    }
  }
};
</script>
<style scoped>
.entire-outboxt {
  width: 500px;
}
</style>