<template>
    <v-card flat :min-height="150" color="#f5f5f5" class="board_adv_values" v-if="meta!=null">
        <v-row no-gutters>
            <v-col :cols="6" class="d-flex justify-center flex-row align-center">
                <div>
                    등록 헬스장 
                    <div class="number_space">
                        <ICountUp :delay="delay" :endVal="meta.space" :options="options" />
                    </div>
                </div>
            </v-col>
            <v-col :cols="6" class="d-flex justify-center flex-row align-center">
                <div>
                    활동지수
                    <div class="number_space">
                        <ICountUp :delay="delay" :endVal="meta.board" :options="options"  /> 게시글 /
                        <ICountUp :delay="delay" :endVal="meta.reply" :options="options" /> 리플
                    </div>
                </div>
            </v-col>
        </v-row>
        <v-row no-gutters>
            <v-col :cols="6">
                <div>
                    유저수
                    <div class="number_space">
                        <ICountUp :delay="delay" :endVal="meta.user" :options="options" />
                    </div>
                </div>
            </v-col>
            <v-col :cols="6">
                <div>
                    리뷰수
                    <div class="number_space">
                        <ICountUp :delay="delay" :endVal="meta.review" :options="options" />
                    </div>
                </div>
            </v-col>
        </v-row>
    </v-card>
</template>
<script>
    import ICountUp from 'vue-countup-v2';
    export default {
        components: {
            ICountUp
        },
        props:{
            meta: Object,
        },
        data() {
            return {
                delay: 300,
                options: {
                    useEasing: true,
                    useGrouping: true,
                    separator: ',',
                    decimal: '.',
                    prefix: '',
                    suffix: ''
                }
            }
        },
    }
</script>
<style scoped>
.number_space{
    color:rgb(128, 140, 247);
    font-size: 24px;
}
@media screen and (max-width: 768px) { 
    .number_space { font-size: 16px; } 
}
.board_adv_values{
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
}
</style>