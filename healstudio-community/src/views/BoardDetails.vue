<template>
    <v-layout wrap class="board_page_layout">
        <v-flex xs12 sm8 md8>
            <v-card class="ma-3 pa-3" height=300>
            <v-card-title class="board_page_title">
                자유게시판
            </v-card-title>
            <v-divider />
                {{$route.params.id}}
                {{$route.query.user}}
            </v-card>
        </v-flex>
    </v-layout>
</template>