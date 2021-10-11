<template>
    <v-card class="ma-3 pa-3">
        <!-- {{data}} -->
        <div v-for="review, key in data" :key="key">
            <div>
                {{review.gymInfo.name}}
            </div>
            <div>
                {{review.user}}
            </div>
            <div>
                {{review.point}}
            </div>
            <div>
                {{review.contents}}
            </div>
        </div>
    </v-card>
</template>
<script>
export default {
    props: {
        data: Array,
    },
}
</script>