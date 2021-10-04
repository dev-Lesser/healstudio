<template>
<div style="display: flex; justify-contents: center;">
<v-layout wrap>
        <side-nav-bar />
        <gym-detail :data="gyms"/>
        <l-map id="map" :zoom="zoom" :center="center">
            <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
            
            <l-marker  :lat-lng="markerLatLng"></l-marker>
            <!-- <div v-if="locations">
                <l-marker v-for="key in latlon" :key="key" :lat-lng="latlon[key]"></l-marker>
            </div> -->
            <!-- <v-marker v-for="key in locations" :key="`marker__${key}`" :lat-lng="locations[key]">
            
            </v-marker> -->
        </l-map>
        
</v-layout>
</div>
</template>
<script>
import "leaflet/dist/leaflet.css"
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
// import * as Vue2Leaflet from 'vue2-leaflet'

import GymDetail from "@/components/GymDetail"
import SideNavBar from '@/components/SideNavBar'
import { Icon } from 'leaflet';
import { search_by_query } from '@/assets/api'
export default {
    components: {
        LMap,
        LTileLayer,
        LMarker,
        // 'v-marker': Vue2Leaflet.LMarker,
        GymDetail,
        SideNavBar,
        
    },
    data(){
        return {
            drawer: true,
            sheet: false,
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            attribution: '',
            zoom: 12,
            center: [37.555, 127.019],
            markerLatLng:[37.555, 127.019],
            latlon: null,
        }
    },
    
    async created() {
        delete Icon.Default.prototype._getIconUrl;
        Icon.Default.mergeOptions({
        iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
        iconUrl: require('leaflet/dist/images/marker-icon.png'),
        shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
        });
        // await this.getGymList(1);
    },
    async mounted(){
        

    },
    async beforeUpdate(){
       
            
        
    },
    computed: {
        gyms(){
            return this.$store.state.selectedData;
        },
        locations(){
            return this.$store.state.locations;
        }
    },
    methods:{
        async getGymList(skip) {
            this.loading = true
            const skipCount = (skip - 1) * 20
            const [success, gyms] = await search_by_query(this.query, skipCount, 20);
            const locations = gyms.map(e => {
                return [e.y, e.x] // 반대임
            });
            this.$store.state.locations = locations;
            if (!success) this.status = -1;
            else {
                this.$store.state.gyms = gyms
                this.loading = false;
            }
        }
    },
    watch:{
        gyms(){
            // console.log(this.$store.state.gyms)
        },
        locations(){
            console.log(123)
            // this.latlon=this.$store.state.locations.map(e => {
            //     return e
            // });
            // this.$store.state.locations = this.latlon;
            // for(var key in this.latlon){
            //     console.log(this.latlon[key])
            // }
            
        }
    }
}
    
</script>
<style scoped>
#map{
    height: calc(100vh - 64px);
    width: calc(100vw - 360px);
}
</style>