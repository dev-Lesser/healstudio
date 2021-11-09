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
    name: "Pagination",
    data() {
        return {
            loading: false,
            start: 1,
            current: 1,
            limit: Math.ceil(this.total/this.length),
            tmpBoards: this.boards,
            user_id: this.$route.params.id,
            view: 5
        }
    },
    
    props:{
        total: Number,
        length: Number
    },
    computed:{
        pages: function () {
            return Array.from(
                { length: this.end - this.start +1},
                (e, i) => i + this.start
                
            );
        },
        end: function(){
            return Math.min(this.start + this.length -1, this.limit)
        },
        
    },
    watch:{
        total: function(newtotal){
            this.start = 1;
            this.current = 1;
            this.limit = Math.ceil(newtotal / this.view);
        },
        view: function (newview) {
            this.limit = Math.ceil(this.total / newview);
        },
    },
    methods:{
        async selectGym(gym) {
            this.$store.state.selected = false
            this.$store.state.selectedData = gym;
            this.$store.state.selected = true;
        },
        async handlePageClick(page) {
            if (this.current == page) return
            this.loading = true;
            this.current = page;
            this.$emit("page-click", page);
        },
        async handlePrevClick() {
            if (this.start == 1)  return;
            this.loading = true;
            const current = this.start - this.length;
            this.start = current;
            this.end = this.start + this.length -1
            this.$emit("page-click", current);
        },
        async handleNextClick() {
            if (this.end == this.limit) return;
            this.loading = true;
            const page = this.start + this.length;
            this.start = page;
            this.end = this.start + this.length -1
            this.current = page;
            this.$emit("page-click", page);
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