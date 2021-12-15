<template>
    <v-navigation-drawer 
    class="nav-drawer" 
    v-if="showMenu"
    v-model="drawer" 
    permanent
    app
    width='360px' 
    color="rgba(208, 208, 228, 0.4)">
        <div class="sidenav-fix">
            <div class="sidenav-title" onclick="location.href='/';">
                <v-list-item-title class="sidenav-header">HEALSTUDIO</v-list-item-title>
            </div>
            <v-divider/>
            <v-list dense>
                <v-list-item>
                    <v-list-item-content>
                        <v-text-field 
                        class="search-text-field"
                        v-model="query"
                        @keydown.enter="searchByQuery" 
                        placeholder="주변 헬스장 검색" rounded outlined dense prepend-inner-icon="mdi-map-marker"></v-text-field>
                    </v-list-item-content>
                </v-list-item>
                <v-divider />
            </v-list>
        </div>
        
        <v-list dense v-if="status!=-1">
            <perfect-scrollbar>
                <v-list-item v-for="gym, key in gyms" :key="key">
                    <v-list-item-content>
                        <div class="data-header">
                            <div class="data-header-name">
                                <div>
                                    {{ gym.name }}
                                </div>
                                <div class="data-header-detail">
                                    <v-chip class="mt-2" x-small>{{ gym.category}}</v-chip>
                                    <div class="rate-content">
                                        <v-rating v-model="rating" background-color="white" color="yellow accent-4" dense half-increments size="18" readonly></v-rating>
                                        <div class="rate-content">
                                            {{ rating }}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <v-spacer />
                            <v-btn v-if="gym.bookingUrl!=null" :href="gym.bookingUrl" outlined small color="green">
                                예약
                            </v-btn>
                            <v-btn outlined small color="purple" @click="selectGym(key)">
                                자세히
                            </v-btn>
                        </div>
                        <div>
                            <div class="data-content-address">{{ gym.fullAddress}}</div>
                        </div>
                        <v-card>
                            <v-img :src="gym.imageUrl" height="200">
                                <v-chip v-if="gym.region_detail_spec!=null" class="image-region-tag" small>{{gym.region}} {{gym.region_detail}} {{gym.region_detail_spec}}</v-chip>
                                <v-chip v-else class="image-region-tag" small>{{gym.region}} {{gym.region_detail}} </v-chip>
                                
                                
                            </v-img>
                            
                            <v-expansion-panels flat dense>
                                <v-expansion-panel>
                                    <v-expansion-panel-header class="data-businesshour">
                                        영업시간
                                    </v-expansion-panel-header>
                                    <v-expansion-panel-content class="data-businesshour-content" v-for="data, ikey in gym.businessHours.split('|')" :key="ikey">
                                        {{ data }}
                                    </v-expansion-panel-content>
                                </v-expansion-panel>
                            </v-expansion-panels>
                        </v-card>
                        <v-divider class="mt-3" />
                    </v-list-item-content>
                </v-list-item>
            </perfect-scrollbar>
            <!-- 가상 스크롤바 -->

            <v-progress-linear
            indeterminate
            color="black"
            class="mt-12"
            v-if="loading"
            ></v-progress-linear>
            <v-progress-linear
            color="black"
            class="mt-3"
            v-else
            ></v-progress-linear>
            <div class="d-flex flex-row justify-center">
                <v-icon class="pagination_page" @click="handlePrevClick" :color="start == 1 ? '#adadad' : '#757575'">mdi-chevron-left</v-icon>
                <div class="pagination_page d-flex flex-row justify-center align-center" 
                v-for="p in pages" :key="p" 
                :class="{ selected_page: current == p }" 
                @click="handlePageClick(p)">
                    {{ p }}
                </div>
                <v-icon class="pagination_page" @click="handleNextClick" :color="end == limit ? '#adadad' : '#757575'">mdi-chevron-right</v-icon>
            </div>
        </v-list>
        <v-list v-else >
            <v-card>
                데이터가 존재하지 않습니다
            </v-card>
        </v-list>
    </v-navigation-drawer>
</template>
<script>
    // import Paginate from 'vuejs-paginate'
    import {
        get_region_list,
        search_by_query,
    } from '@/assets/api'
    export default {
        components: {
            // Paginate
        },
        data() {
            return {
                query: '',
                loading: false,
                page: 1,
                total: 10,
                perpage: 5,
                showMenu: true,
                regions: null,
                drawer: true,
                mini: true,
                businessHours: null,
                rating: 4.1,
                limit: 30,
                start: 1,
                current: 1,
                length: 5,
                status: 1,
            }
        },
        async created() {
            const [success, regions] = await get_region_list();
            // console.log(status, data)
            if (!success) this.status = -1;
            // No contents
            else {
                this.regions = regions
            }
            this.loading = false;
        },
        async mounted() {
            await this.getGymList(1) // init
        },
        computed: {
            gyms() {
                return this.$store.state.gyms;
            },
            end: function() {
                return Math.min(this.start + this.length - 1, this.limit);
            },
            pages: function() {
                return Array.from({
                        length: this.end - this.start + 1
                    },
                    (e, i) => i + this.start
                );
            },
        },
        watch: {
            total: function(newtotal) {
                this.$emit("page-click", 1);
                this.start = 1;
                this.current = 1;
                this.limit = Math.ceil(newtotal / this.view);
            },
            view: function(newview) {
                this.limit = Math.ceil(this.total / newview);
            },
        },
        methods: {
            async searchByQuery(event){
                event.preventDefault() 
                this.$store.state.selected = false;
                this.loading = true
                const skipCount = (this.current - 1) * 20
                
                const [success, gyms] = await search_by_query(this.query, skipCount, 20);
                if (!success) {
                    console.log(success)
                    this.status = -1;
                }
                else {
                    this.$store.state.gyms = gyms
                    
                }

                this.loading = false;
            },
            async handlePageClick(page) {
                this.loading = true;
                this.current = page;
                await this.getGymList(this.current)
            },
            async handlePrevClick() {
                this.loading = true;
                if (this.start == 1) return;
                const current = this.start - this.length;
                this.start = current;
                this.current = current;
                await this.getGymList(this.current)
            },
            async handleNextClick() {
                this.loading = true;
                if (this.end == this.limit) return;
                const page = this.start + this.length;
                this.start = page;
                this.current = page;
                await this.getGymList(this.current)
                
            },
            async selectGym(idx) {
                this.$store.state.selected = false
                this.$store.state.selectedData = this.gyms[idx];
                this.$store.state.selected = true;
            },
            async getGymList(skip) {
                this.loading = true
                const skipCount = (skip - 1) * 20
                const [success, gyms] = await search_by_query(this.query, skipCount, 20);
                if (!success) this.status = -1;
                else {
                    console.log(gyms)
                    this.$store.state.gyms = gyms
                    this.loading = false;
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
    .sidenav-title {
        color: white;
        padding: 30px 20px;
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
    .thumbnail-img {
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
        font-family: 'Jeju Gothic', sans-serif;
    }
    .data-content-address {
        font-size: 13px;
        margin: 10px;
        font-family: 'Jeju Gothic', sans-serif;
    }
    .search-text-field,
    .data-businesshour {
        font-size: 15px;
        font-family: 'Jeju Gothic', sans-serif;
    }
    .data-businesshour-content {
        font-size: 12px;
        font-family: 'Jeju Gothic', sans-serif;
    }
    .rate-content {
        font-size: 12px;
        display: flex;
        align-content: center;
        align-items: center;
        justify-content: left;
    }
    .data-header-detail {
        display: inline;
    }
    .pagination-bar {
        display: inline-block;
        padding-left: 0;
        margin: 20px 0;
        border-radius: 4px;
    }
    .pagination_page {
        cursor: pointer;
        width: 34px;
        height: 34px;
        border-radius: 17px;
        text-align: center;
        margin: 4px;
    }
    .selected_page {
        color: white;
        background-color: #B2C9CF;
    }
    .image-region-tag{
        font-family: 'Jeju Gothic', sans-serif;
        float: right;
        margin-top:5px;
        margin-right:5px;
    }
</style>