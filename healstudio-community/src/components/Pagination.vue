<template>
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
</template>
<script>
export default {
    data() {
        return {
            pages: 5,
            end: 100,
            loading: false,
            start: 1,
            current: 1,
            length: 5,
            limit: 30,
        }
    },
    methods:{
        async handlePageClick(page) {
                if (this.current == page) return
                this.loading = true;
                this.current = page;
        },
        async handlePrevClick() {
            if (this.start == 1)  return;
            this.loading = true;
            const current = this.start - this.length;
            this.start = current;
            this.current = current;
        },
        async handleNextClick() {
            if (this.end == this.limit) return;
            this.loading = true;
            const page = this.start + this.length;
            this.start = page;
            this.current = page;
            // await this.getReviews(this.$route.params.id, (this.current-1)*5, 5)
            
        },
    }
}
</script>
<style>
.pagination-bar {
        display: inline-block;
        padding-left: 0;
        margin: 20px 0;
        border-radius: 4px;
    }
.selected_page {
    color: white;
    background-color: #B2C9CF;
}
.pagination_page {
        cursor: pointer;
        width: 34px;
        height: 34px;
        border-radius: 17px;
        text-align: center;
        margin: 4px;
    }
.bottom_button{
    bottom: 1px;
}
</style>