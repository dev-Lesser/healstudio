<template>
<v-navigation-drawer v-if="selected" 
    class="sheet" 
    absolute 
    left 
    floating 
    hide-overlay 
    color="rgba(250, 250, 250, 0.9)"
    width="350px">
        <v-card-actions>
            <v-spacer />
        <v-icon class="pl-3 mb-2" @click="$store.state.selected = !$store.state.selected">mdi-close</v-icon>
        </v-card-actions>
        <div class="box-title-wrap">
            <div class="box-title">
                <div>
                {{selectedData.name}}
                <show-desc :desc="desc" />
                </div>
                <v-rating
                v-model="rating"
                background-color="white"
                color="yellow accent-4"
                dense
                half-increments
                size="18"
                readonly
                ></v-rating>
                <div class="box-category">
                    <v-chip small outlined>{{selectedData.category}}</v-chip>
                </div>
            </div>
            
        </div>
        

            <v-divider />
            <v-carousel
            cycle
            height="200">
                <v-carousel-item
                v-for="(image,i) in selectedData.imgList"
                :key="i"
                :src="`https://healstudio.s3.ap-northeast-2.amazonaws.com/images/${selectedData.id}/${image}.jpg`"
                reverse-transition="fade-transition"
                transition="fade-transition"
                ></v-carousel-item>
            </v-carousel>
            <!-- <div v-for="image, i in selectedData.imgList"  :key="i">
            <v-img  
            height="300"
            ></v-img> -->
            <!-- </div> -->
            <v-card-subtitle class="box-hashtag-title">
                    # 해시태그
                <div class="box-keywords">
                    <v-chip outlined class="box-hashtag-content ma-2" small v-for="keyword, i in selectedData.keywords" :key="`keyword--${i}`">#{{keyword}}</v-chip>
                </div>
            </v-card-subtitle>
            <v-divider />
            <div class="box-address" >
                <v-icon>mdi-map-marker</v-icon>
                <div class="box-address-info" v-if="selectedRoadAddress">{{selectedData.roadAddress}}</div>
                <div class="box-address-info" v-else>{{selectedData.fullAddress}}</div>
                <v-spacer/>
                <v-btn small @click="selectedRoadAddress = !selectedRoadAddress" >변환</v-btn>
            </div>
            <v-divider />
            <v-card-subtitle style="display:flex;">
                <div class="box-phone">
                    <v-icon small>mdi-phone</v-icon>
                    {{selectedData.phone}}<br/>
                    <div v-if="selectedData.virtualPhone!=null">
                    <v-icon small>mdi-phone</v-icon>
                    {{selectedData.virtualPhone}}</div>
                </div>
                
                <v-spacer />
                <v-btn 
                :href="selectedData.bookingUrl" 
                outlined
                small
                color="green"
                v-show="selectedData.bookingUrl"
                > 
                    예약 
                </v-btn> 
                
            </v-card-subtitle>
            <v-divider />
            <div class="box-businesshour" >
                <div class="box-businesshour-title">  <v-icon class="mt-1 mr-3" small>mdi-timelapse</v-icon>영업 시간</div>
                <v-spacer/>
                <v-menu v-model="info" offset-x open-on-hover>
                    <template v-slot:activator="{ on, attrs }">
                        <div style="display: flex;justify-content: center;align-content: center;">자세히</div>
                    <v-btn v-bind="attrs" v-on="on" text icon>
                        
                        <v-icon>mdi-information-outline</v-icon>
                    </v-btn>
                    </template>
                    <v-card width="300px" class="pa-3">
                    <div class="box-businesshour-sheet-title">영업 시간</div>
                    <div class="box-businesshour-content ma-1 pa-2" v-for="data, ikey in selectedData.businessHours.split('|')" :key="ikey">{{data}}<v-divider /></div>
                    </v-card>
                </v-menu>
                
            </div>
            <v-divider />
            <!--  -->
            
            <div v-for="url, i in selectedData.urlList" :key="`url--${i}`"> 
                <div class="box-hompage">
                    <div  class="box-url-list" v-if="url.type == 'normal' | url.type =='modoo'">

                        <v-icon>mdi-home</v-icon>
                        <div class="box-url ml-3"><a :href="url.url">{{url.url}}</a></div>
                    </div>
                    <div class="box-url-list"  v-else-if="url.type == 'instagram' ">
                        <v-icon color="#E36DEE">mdi-instagram</v-icon>
                        <div class="box-url ml-3"><a :href="url.url">{{url.url}}</a></div>
                    </div>
                    <div class="box-url-list"  v-else-if="url.type == 'facebook' ">
                        <v-icon color="#6B74F1">mdi-facebook</v-icon>
                        <div class="box-url ml-3"><a :href="url.url">{{url.url}}</a></div>
                    </div>
                    <div class="box-url-list"  v-else-if="url.type == 'blog' ">
                        <v-icon>mdi-desktop-mac</v-icon>
                        <div class="box-url ml-3"><a :href="url.url">{{url.url}}</a></div>
                    </div>
                    <div class="box-url-list"  v-else>
                        <v-icon>mdi-cube-outline</v-icon>
                        <div class="box-url ml-3"><a :href="url.url">{{url.url}}</a></div>
                    </div>
                </div>
            </div>
            <div v-for="url, i in selectedData.imgList" :key="`img--${i}`">
                <!-- {{url}}.jpg {{selectedData.imageUrl}} -->
                
            </div>
    </v-navigation-drawer>
</template>
<script>
import ShowDesc from '@/components/ShowDesc'
    export default {
        components:{
            ShowDesc
        },
        data() {
            return {
                info: null,
                rating: 5,
                desc: null,
                selectedRoadAddress: false,
            }
        },
        computed: {
            selected() {
                return this.$store.state.selected;
            },
            selectedData() {
                return this.$store.state.selectedData;
            }
        },
        watch: {
            selectedData() {
                var desc = this.$store.state.selectedData.desc;
                this.desc = desc.replace(/\n/g, '<br/>');
            }
        },
    }
</script>
<style scoped>
.sheet {
    padding: 10px;
    position: absolute;
    z-index: 1000;
    border-width: 1px;
    display: block;
    -ms-overflow-style: none; /* IE and Edge */
    -webkit-transition:width 2s, height 2s, background-color 2s, -webkit-transform 2s;
    transition: all ease 2s 0s;
}
.sheet::-webkit-scrollbar {
    display: none; /* Chrome, Safari, Opera*/
}
.box-hashtag-title{
    font-size: 15px;
    font-family:'Jeju Gothic', sans-serif;
}
.box-hashtag-content{
    background-color: #F00000
}
.box-title-wrap {
    display: flex;
    justify-content: center;
    align-content: center;
}
.box-title {
    text-align: center;
    padding: 5px;
    font-size: 20px;
    font-family:'Jeju Gothic', sans-serif;
}
.box-category {
    font-family:'Jeju Gothic', sans-serif;
}
.box-address{
    display: flex;
    align-items: center;
    padding: 10px;
    font-size: 13px;
    font-family:'Jeju Gothic', sans-serif;
    
}
.box-address-info{
    display: flex;
    padding: 10px;
    align-items: center;
}
.box-booking-url{
    font-size: 13px;
    font-family:'Jeju Gothic', sans-serif;
}
.box-phone {
    font-size: 13px;
    font-family:'Jeju Gothic', sans-serif;
}
.box-businesshour{
    display: flex;
    justify-content: left;
    align-items: center;
    padding: 10px;
    font-size: 13px;
    font-family:'Jeju Gothic', sans-serif;
}
.box-businesshour-sheet-title{
    font-size: 13px;
    font-family:'Jeju Gothic', sans-serif;
}
.box-businesshour-content{
    font-size: 13px;
    font-family:'Jeju Gothic', sans-serif;
}
.box-description{
    font-size: 13px;
    font-family:'Jeju Gothic', sans-serif;
    background-color: azure;
}
.box-keywords{
    width: 300px;
    height: 50px;
    overflow-x: scroll;
    overflow-y: hidden;
    white-space: nowrap;
    scrollbar-width: thin;
}
.box-keywords::-webkit-scrollbar {
    width: 4px;
    scrollbar-width: thin;
}
.box-keywords::-webkit-scrollbar-thumb {
    background-color: #868686;
    border-radius: 15px;
    background-clip: padding-box;
    border: 2px solid transparent;
    scrollbar-width: thin;
  }
.box-keywords::-webkit-scrollbar-track {
    
    background-color: rgb(175, 174, 174);
    border-radius: 15px;
    box-shadow: inset 0px 0px 5px white;
    scrollbar-width: thin;
}
.box-hompage{
    display:flex;
}
.box-url-list{
    margin-top:5px;
    padding: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 5px;
    border: 1px dashed #bcbcbc;
}
/* url list 길이 조정 */
.box-url {
    font-size: 13px;
    font-family:'Jeju Gothic', sans-serif;
    width: 270px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;  /* 말줄임 적용 */
}
</style>