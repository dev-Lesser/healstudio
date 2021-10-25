<template>
    <v-card class="pa-3 ma-3 ">
        <v-card-actions style="">
            <v-flex xs12 md6 style="display:grid;justify-content:center;">
                <div stlye="display:grid;justify-content:center;">
                <v-avatar  color="indigo" size="100" >
                    <v-icon dark size="60">
                        mdi-account-circle
                    </v-icon>
                </v-avatar>
                </div>
                <v-card-subtitle>
                        아이디 : {{userMeta.user}}
                    </v-card-subtitle>
            </v-flex>
            <v-spacer/>
            <v-flex xs12 md6 >
                <v-row class="display_contents">
                    <v-col>
                        <div>
                            찜한 헬스장 개수 
                        </div>
                    </v-col>
                    <v-col>
                        <div class="display_number_box">
                            <ICountUp :delay="delay" :endVal="favGymLenth" :options="options" />
                        </div>
                    </v-col>
                </v-row>
                <v-divider />
                <v-row class="display_contents">
                    <v-col>
                        <div>
                            리뷰 개수
                        </div>
                    </v-col>
                    <v-col>
                        <div class="display_number_box">
                            <ICountUp :delay="delay" :endVal="reviewsLenth" :options="options" />
                        </div>
                    </v-col>
                </v-row>
                <v-divider />
                <v-row class="display_contents">
                    <v-col>
                        <div>
                        IP
                        </div>
                    </v-col>
                    <v-col>
                        <div >
                            <v-text-field
                            class="ma-2"
                                style="display:flex; justify-content:center;"
                                :value="userMeta.ip"
                                readonly
                                disabled
                                dense
                                outlined
                                hide-details
                            ></v-text-field>
                        </div>
                    </v-col>
                </v-row>
                <v-divider />
                <v-row class="display_contents">
                    <v-col class="display_login">
                        <div>
                        회원가입: {{userMeta.created_at}}
                        </div>
                    </v-col>
                    <v-col class="display_login">
                    <div>
                    최근로그인: {{userMeta.last_login}}
                    </div>
                    </v-col>
                </v-row>
            </v-flex>
        </v-card-actions>
    </v-card>
</template>
<script>
import ICountUp from 'vue-countup-v2';
        
export default {
    props: {
        userMeta: Object,
        favGymLenth: Number,
        reviewsLenth: Number

    },
    components: {
        ICountUp
    },
    data(){
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
    }
}
</script>
<style scoped>
.display_number_box{
    font-size:36px;
    color: rgb(247, 137, 64)
}
.display_contents{
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
}
.display_login{
    font-size: 12px;
    color: rgb(175, 171, 171);
}
</style>