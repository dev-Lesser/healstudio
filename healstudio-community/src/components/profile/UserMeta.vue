<template>
    <v-card class="pa-3 ma-3">
        <v-avatar  color="indigo" size="100">
            <v-icon dark size="60">
                mdi-account-circle
            </v-icon>
        </v-avatar>
        <v-card-subtitle>
            아이디 : {{userMeta.user}}
        </v-card-subtitle>
        <v-card-subtitle>
            찜한 헬스장 개수 : {{favGymLenth}}
        </v-card-subtitle>
        <v-card-subtitle>
            내가 쓴 리뷰 개수 : {{reviewsLenth}}
        </v-card-subtitle>
        ip : {{userMeta.ip}}
        회원가입: {{userMeta.created_at}}
        최근로그인: {{userMeta.last_login}}
    </v-card>
</template>
<script>
export default {
    props: {
        userMeta: Object,
        favGymLenth: Number,
        reviewsLenth: Number

    },
}
</script>