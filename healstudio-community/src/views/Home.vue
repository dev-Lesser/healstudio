<template>
<div style="display: flex; justify-contents: center;">
<v-layout wrap>
        <side-nav-bar />
        <gym-detail :data="gyms"/>
        <l-map id="map" :zoom="zoom" :center="center">
            <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
            <l-marker :lat-lng="markerLatLng"></l-marker>
        </l-map>
        
</v-layout>
</div>
</template>
<script>
import "leaflet/dist/leaflet.css"
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
import GymDetail from "@/components/GymDetail"
import SideNavBar from '@/components/SideNavBar'
import { Icon } from 'leaflet';

export default {
    components: {
        LMap,
        LTileLayer,
        LMarker,
        GymDetail,
        SideNavBar
        
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
        }
    },
    
    async created() {
        delete Icon.Default.prototype._getIconUrl;
        Icon.Default.mergeOptions({
        iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
        iconUrl: require('leaflet/dist/images/marker-icon.png'),
        shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
        });
    // HERE is where to load Leaflet components!
        // const { circleMarker } = await import("leaflet/dist/leaflet-src.esm");

        // And now the Leaflet circleMarker function can be used by the options:
        // this.geojsonOptions.pointToLayer = (feature, latLng) =>
        // circleMarker(latLng, { radius: 8 });
        // this.mapIsReady = true;
    },
    async mounted(){
    },
    computed: {
        gyms(){
            return this.$store.state.selectedData
        }
    },
    watch:{
        gyms(){
            // console.log(this.$store.state.gyms)
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