<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>
          Lowfound OpenAI API Chat
        </q-toolbar-title>
        <q-btn v-if="$route.path == '/'"  @click="deleteToken()">
          Logout
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { apiAxios } from 'src/boot/axios';
import { LocalStorage } from "quasar";
import { useRouter } from "vue-router";
const router = useRouter();

function deleteToken(){
  LocalStorage.remove("myString");

  router.push("/auth").then(() => {
    window.location.reload();
   });
}

</script>

<style lang="scss">

</style>
