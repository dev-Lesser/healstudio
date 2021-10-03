<template>
    <div class="login">
        <div class="login-card">
            <div id="menu_logo" style="cursor: default">
                <div id="menu_logo_letter">
                    HEALSTUDIO
                </div>
                <div id="menu_logo_circle" />
                
            </div>
            <v-divider />
            <div class="intro_box" >
                HEALSTUDIO 는 전국에 있는 헬스장과 관련하여 정보를 제공하고 사용자간의 대화를 통해 정보교환을 할 수 있는 커뮤니티 사이트 입니다.
            </div>
            <v-form class="login-form">
                <v-text-field v-model="id" color="#52abc4" dense outlined label="아이디" @keyup.enter="doLogin" />
                <v-btn block dark class="mb-5"> 중복여부체크 </v-btn>
                <v-text-field v-model="pw" color="#52abc4" dense outlined label="비밀번호" type="password" @keyup.enter="doLogin" />
                <v-text-field v-model="pwCheck" color="#52abc4" dense outlined label="비밀번호 확인" type="password" @keyup.enter="doLogin" />
                <v-btn class="login-btn-submit" color="#52abc4" dark @click="doLogin">
                    회원가입
                </v-btn>
                
            </v-form>
        </div>
    </div>
</template>
