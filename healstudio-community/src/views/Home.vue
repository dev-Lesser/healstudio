<template>
<div style="display: flex; justify-contents: center;">
<v-layout wrap>
        <side-nav-bar />
        <gym-detail :data="gyms"/>
        <l-map id="map" :zoom="zoom" :center="center">
            <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
            
            <l-marker  :lat-lng="markerLatLng"></l-marker>
            <l-marker v-for="item,key in locations" :key="key" :lat-lng="item"></l-marker>
            
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
            latlon: [[37.555, 127.019],[37.755, 127.019],[37.255, 127.019],[37.415, 127.019],[37.555, 126.019],],
        }
    },
    
    async created() {
        delete Icon.Default.prototype._getIconUrl;
        Icon.Default.mergeOptions({
        iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
        iconUrl: require('leaflet/dist/images/marker-icon.png'),
        shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
        });
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
    },
    watch:{
        gyms(){
        },
        locations(){
            
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