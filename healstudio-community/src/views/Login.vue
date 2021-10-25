<template>
    <div class="login">
        <div class="login-card">
            <div id="menu_logo" style="cursor: default">
                <div id="menu_logo_letter">
                    HEALSTUDIO
                </div>
                <div id="menu_logo_circle" />
            </div>
            <v-form class="login-form">
                <v-text-field v-model="id" color="#52abc4" dense outlined label="아이디" @keyup.enter="doLogin" />
                <v-text-field style="font-family:'Noto Sans', sans-serif;" v-model="pw" color="#52abc4" dense outlined label="비밀번호" type="password" @keyup.enter="doLogin" />
                <v-btn class="login-btn-submit" color="#52abc4" dark @click="doLogin">
                    로그인
                </v-btn>
                <v-divider class="mb-3"/>
                아직 회원이 아니세요?
                <v-btn class="signup-btn-submit" color="#20738A" dark @click="gotoSignUp">
                    회원가입
                </v-btn>
            </v-form>
        </div>
    </div>
</template>

<script>
    // import bcrypt from "bcrypt-nodejs"; //# todo
    import { login } from "@/assets/auth";
    export default {
        data: () => ({
            id: null,
            pw: null,
        }),
        methods: {
            async doLogin() {
                const [issuccess, res] = await login(this.id, this.pw);
                if (!issuccess) {
                    alert("아이디와 비밀번호를 확인해주세요.");
                    return;
                }
                window.localStorage.setItem("user_id", res.user_id);
                window.localStorage.setItem("token", res.token);
                this.$router.push("/");
                
            },
            async gotoSignUp(){
                this.$router.push("/signup");
            }
        },
    };
</script>

<style>
    .login {
        width: 100vw;
        height: calc(100vh - 60px);
        display: flex;
        justify-content: center;
        align-items: center;
        background: #f5f5f5;
    }
    .login-card {
        width: 500px;
        height: 680px;
        box-shadow: 5px 5px 6px 0 rgba(0, 0, 0, 0.16);
        background-color: #ffffff;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    #menu_logo_letter{
        font-family:'Jeju Gothic', sans-serif;
        font-size: 30px;
        font-weight: bold;
    }
    .login-form {
        font-family:'Jeju Gothic', sans-serif;
        width: 320px;
        margin-top: 30px;
        color: black,
    }
    .login-btn-submit {
        margin-top: 100px;
        margin-bottom: 10px;
        width: 320px;
    }
    .signup-btn-submit {
        margin-top: 10px;
        width: 320px;
    }
</style>