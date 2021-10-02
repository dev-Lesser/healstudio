<template>
    <v-navigation-drawer 
    class="nav-drawer" 
    v-if="showMenu" 
    v-model="drawer" 
    app 
    width='350px' 
    color="rgba(208, 208, 228, 0.4)"
    >
    
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
        <v-list-item  v-for="gym, key in gyms" :key="key" >
            <v-list-item-content>
                <!-- {{gym}} -->
                
                <v-card-subtitle class="data-header">
                    <div class="data-header-name">
                        <div>
                        {{ gym.name }} 
                        </div>
                         <v-chip class="mt-2" x-small>{{ gym.category}}</v-chip>
                         <v-rating
                        v-model="rating"
                        background-color="purple lighten-3"
                        color="purple"
                        x-small
                        ></v-rating>
                        <div>
                            {{ rating }}
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
                    > 
                    자세히 
                    </v-btn>
                </v-card-subtitle>
                
                
                <v-card-subtitle class="data-content-address">{{ gym.fullAddress}}</v-card-subtitle>
                <v-card>
                    <v-img 
                    :src="gym.imageUrl"></v-img>
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
                
                
                
                
                
                
                <!-- {{ gym.desc}} -->
                <v-divider class="mt-3"/>
            </v-list-item-content>
            
        </v-list-item>
    </v-list>
  </v-navigation-drawer>
      
</template>
<script>


import { get_region_list, get_gyms_list } from '@/assets/api'

export default {
    data() {
        return {
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
            console.log(regions)
        }
        this.loading = false;
    },
    async mounted(){
        await this.getGymList()
    },
    methods:{
        async parseBusinessHours(data){
            const res = data.split('|');
            console.log(res)
        },
        async getGymList(){
            const [success, gyms] = await get_gyms_list(0, 10);
            if (!success) this.status = -1;
            else {
                this.gyms = gyms
                this.parseBusinessHours('평일 07:00~22:00 | 일요일 10:00~22:00 PT의 경우 주말에도 수업합니다. 소그룹 PT는 일요일 오전10시에 한타임진행하고 있습니다.')
                // console.log(this.gyms)
            }
        }
    }
}
</script>
<style scoped>
@import url(//fonts.googleapis.com/earlyaccess/jejugothic.css);
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
    font-size: 20px;
    font-family:'Jeju Gothic', sans-serif;

}
.data-content-address{
    font-size: 15px;
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
</style>