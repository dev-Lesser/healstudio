<template>
    <v-navigation-drawer 
    class="nav-drawer" 
    v-if="showMenu" 
    v-model="drawer" 
    app 
    width='350px' 
    color="rgba(208, 208, 228, 0.4)"
    >
    <div class="sidenav-fix">
        <div class="sidenav-title" onclick="location.href='/';">
            <v-list-item-title class="sidenav-header">HEALSTUDIO</v-list-item-title>
        </div>
        
        <v-divider/>
        <v-list dense>
            <v-list-item>
                <v-list-item-content>
                    <v-text-field
                        placeholder="주변 헬스장 검색"
                        rounded
                        outlined
                        dense
                        prepend-inner-icon="mdi-map-marker"
                    ></v-text-field>
                </v-list-item-content>
            </v-list-item>
            <v-divider />
        </v-list>
    </div>
    
        
    
    <v-list dense>
        <perfect-scrollbar>
        <v-list-item  v-for="gym, key in gyms" :key="key" >
        
            <v-list-item-content>
                
                <div class="data-header">
                    <div class="data-header-name">
                        <div>
                        {{ gym.name }} 
                        </div>
                        <div class="data-header-detail">
                            <v-chip class="mt-2" x-small>{{ gym.category}}</v-chip>

                            <div class="rate-content">
                            <v-rating
                            v-model="rating"
                            background-color="white"
                            color="yellow accent-4"
                            dense
                            half-increments
                            size="18"
                            readonly
                            ></v-rating>
                            <div class="rate-content">
                                {{ rating }} 
                            </div>
                        </div>
                    </div>
                    </div>
                
                    <v-spacer />
                    <v-btn 
                    v-if="gym.bookingUrl!=null" 
                    :href="gym.bookingUrl" 
                    outlined
                    small
                    color="green"
                    > 
                        예약 
                    </v-btn>
                    <v-btn 
                    outlined
                    small
                    color="purple"
                    @click="selectGym(key)"
                    > 
                    자세히 
                    </v-btn>
                </div>
                <div>
                    
                    <div class="data-content-address">{{ gym.fullAddress}}</div>
                </div>
                
                <!-- <v-card-subtitle class="data-content-address">{{ gym.fullAddress}}</v-card-subtitle> -->
                <v-card>
                    <v-img 
                    :src="gym.imageUrl" height="200"></v-img>
                    <v-expansion-panels
                    flat
                    dense
                    >
                        <v-expansion-panel >
                        <v-expansion-panel-header  class="data-businesshour" >
                            영업시간
                        </v-expansion-panel-header>
                        <v-expansion-panel-content class="data-businesshour-content" v-for="data, ikey in gym.businessHours.split('|')" :key="ikey">
                            {{ data }}
                        </v-expansion-panel-content>
                        </v-expansion-panel>
                    </v-expansion-panels>

                </v-card>
                
                <v-divider class="mt-3"/>
            </v-list-item-content>
        </v-list-item>
        </perfect-scrollbar>
        <v-list-item >
            <v-pagination
              v-model="page"
              class="my-4"
              :length="15"
            ></v-pagination>
        </v-list-item>
    </v-list>

</v-navigation-drawer>

</template>
<script>


import { get_region_list, get_gyms_list} from '@/assets/api'

export default {
    data() {
        return {
            page: 1,
            showMenu: true,
            regions : null,
            drawer: true,
            mini: true,
            gyms: null,
            businessHours: null,
            rating: 4.1,
        }
        
    },
    async created(){
        const [success, regions] = await get_region_list();
        // console.log(status, data)
        if (!success) this.status = -1;
        // No contents
        else {
            this.regions = regions
        }
        this.loading = false;
    },
    async mounted(){
        await this.getGymList()
    },
    methods:{
        pagination(page){
            console.log(page)
        },
        async selectGym(idx){
            this.$store.state.selected = false
            this.$store.state.selectedData = this.gyms[idx];
            this.$store.state.selected = true;
        },
        // async parseBusinessHours(data){
        //     const res = data.split('|');
        // },
        async getGymList(){
            const [success, gyms] = await get_gyms_list(0, 10);
            if (!success) this.status = -1;
            else {
                this.gyms = gyms
                // console.log(this.gyms)
            }
        }
    }
}
</script>
<style scoped>
@import url(//fonts.googleapis.com/earlyaccess/jejugothic.css);
.ps {
  height: 70vh;
}
.sidenav-fix{
    /* position: absolute; */
    /* height: 350px; */
}
.sidenav-title {
    color: white;
    padding: 40px 20px;
    font-weight: bold;
    font-size: 18px;
}
.sidenav-header {
    color: rgb(124, 115, 115);
    font-size: 25px;
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
}
.nav-drawer {
    background-color: rgba(208, 208, 228, 0.4);
}
.thumbnail-img{
    border-radius: 15px;
}
.data-header {
    display: flex;
    justify-content: center;
    align-content: center;
}
.data-header-name {
    padding: 13px;
    font-size: 20px;
    font-family:'Jeju Gothic', sans-serif;

}
.data-content-address{
    font-size: 13px;
    font-family:'Jeju Gothic', sans-serif;

}
.data-businesshour{
    font-size: 15px;
    font-family:'Jeju Gothic', sans-serif;
}
.data-businesshour-content{
    font-size: 12px;
    font-family:'Jeju Gothic', sans-serif;
}
.rate-content{
    font-size: 12px;
    display: flex;
    align-content: center;
    align-items: center;
    justify-content: left;
}
.data-header-detail{
    display: inline;
}
</style>