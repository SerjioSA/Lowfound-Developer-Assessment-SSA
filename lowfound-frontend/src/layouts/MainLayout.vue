<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>
          Lowfound OpenAI API Chat
        </q-toolbar-title>
        <q-btn @click="onDelete()">
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

function onDelete(){
  apiAxios.delete("/questions")
}
</script>

<style lang="scss">

</style>
