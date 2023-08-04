<template>
<q-page id="AuthStyle" >
  <!-- class="flex flex-center" -->
  <div class="row full-width ">
    <div class="col">
      <div>
        <q-img
          src="~/assets/AuthPhoto.png"
style="height: "
        />
      </div>
      <div>
      <div class="q-pa-md q-gutter-md">
        <!-- <div class="text-center">Register and get extra features!</div> -->

        <q-input
          v-model="usernameLogin"
          :error="hasErrorUsernameLogin"
          :error-message="errorUsernameLogin"
          outlined
          stack-label
          label="Usernsme"
        >
        </q-input>
        <q-input
          :type="isPwd ? 'password' : 'text'"
          v-model="passwordLogin"
          :error="hasErrorPasswordLogin"
          :error-message="errorPasswordLogin"
          outlined
          stack-label
          label="Password"
        >
          <template v-slot:append>
            <q-icon
            :name="isPwd ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPwd = !isPwd"
            />
          </template>
        </q-input>
      </div>
      <div class="q-mx-md">
        <q-btn
          @click="sendComponentDataLogin()"
          color="primary"
          label="Login"
          size="lg"
          class="full-width">
        </q-btn>
    </div>
    <div class="flex flex-center q-mt-md">Or sign up if you don’t have an account yet:</div>
      <div class="q-pa-md q-gutter-md">
        <!-- <div class="text-center">Register and get extra features!</div> -->

        <q-input
          v-model="usernameReg"
          :error="hasErrorUsernameReg"
          :error-message="errorUsernameReg"
          outlined
          stack-label
          label="Username"
        >
        </q-input>
        <q-input
          :type="isPwd ? 'password' : 'text'"
          v-model="passwordReg"
          :error="hasErrorPasswordReg"
          :error-message="errorPasswordReg"
          outlined
          stack-label
          label="Password"
        >
          <template v-slot:append>
            <q-icon
            :name="isPwd ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPwd = !isPwd"
            />
          </template>
        </q-input>
      </div>
      <div class="q-mx-md">
        <q-btn
          @click="sendComponentDataReg()"
          color="primary"
          label="Sign up"
          size="lg"
          class="full-width">
        </q-btn>
    </div>
    </div>

    </div>
  </div>
</q-page>
</template>

<script setup>
import { apiAxios } from "boot/axios";
import { LocalStorage } from "quasar";
import { ref } from "vue";

import { useRouter } from "vue-router";
const router = useRouter();

const passwordLogin = ref("");
const usernameLogin = ref("");
const passwordReg = ref("");
const usernameReg = ref("");

const tokenData = ref("");

const errorMessage = ref("");

const errorUsernameLogin = ref("");
const errorUsernameReg = ref("");

const errorPasswordLogin = ref("");
const errorPasswordReg = ref("");

const hasErrorUsernameLogin = ref(false);
const hasErrorUsernameReg = ref(false);
const hasErrorPasswordLogin = ref(false);
const hasErrorPasswordReg = ref(false);
const isPwd = ref(true);



function sendComponentDataLogin() {
  const data = {
    email: "delet_this",
    password: passwordLogin.value,
    username: usernameLogin.value,
  };

  hasErrorUsernameLogin.value = false;
  hasErrorPasswordLogin.value = false;
  errorUsernameLogin.value = "";
  errorPasswordLogin.value = "";

  apiAxios
    .post("/token/", data)
    .then((response) => {
      tokenData.value = response.data.access_token;
      LocalStorage.set("myString", tokenData.value);
      console.log(tokenData.value)

      router.push("/").then(() => {
        window.location.reload();
      });
    })
    .catch((err) => {
      if (err.response) {
        errorMessage.value = err.response.data.detail;

        hasErrorUsernameLogin.value = true;
        hasErrorPasswordLogin.value = true;
        errorUsernameLogin.value = errorMessage.value;
        errorPasswordLogin.value = errorMessage.value;
      }
    });
}

function sendComponentDataReg() {
  const data = {
    email: "delet_this",
    password: passwordReg.value,
    username: usernameReg.value,
  };

  apiAxios
    .post("/register/", data)
    .then((response) => {
      tokenData.value = response.data.auth_token;
      LocalStorage.set("myString", tokenData.value);

      errorUsernameReg.value = "";
      hasErrorUsernameReg.value = false;

      apiAxios
      .post("/token/", data)
      .then((response) => {
        tokenData.value = response.data.access_token;
        LocalStorage.set("myString", tokenData.value);
        console.log(tokenData.value)

        router.push("/").then(() => {
        window.location.reload();
      });
      })

    })
    .catch((err) => {
      if (err.response) {
        // The client was given an error response (5xx, 4xx)
        // console.log(err.response.data);
        // console.log(err.response.status);
        // console.log(err.response.headers);
        errorMessage.value = err.response.data.detail;

        errorUsernameReg.value = errorMessage.value;
        hasErrorUsernameReg.value = true;


      }
    });
}

</script>

<style lang="scss">
#AuthStyle{
  .scrollStyle{
    height: 40vh;
    width: 100%;
  }
}
</style>
