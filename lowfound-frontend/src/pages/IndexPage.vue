<template>
  <q-page id="IndexStyle" class="flex flex-center">
    <div class="row full-width full-height q-pa-sm">
      <div class="col">

        <q-scroll-area ref="mainScrollArea" class="scrollStyle q-pb-md">
          <div class="text-subtitle1 q-mx-sm" v-if="checkEmptyCards()">Your chat is empty. Send your first message to start a chat.</div>
          <div>
            <q-card  v-for="item in questionCards" :key="item.id" class="cardStyle full-width bg-grey-3 q-ma-sm">

              <q-card-section >
                <div class="text-grey-6 q-py-sm" >{{item.date}}</div>

                <div class="text-blue-6">You asked:</div>
                <p>{{ item.question }}</p>

                <div class="text-blue-6">GPT responded:</div>
                <p>{{ item.answer }}</p>
                <q-btn flat padding="none" @click="item.onClick" class="text-red">Delete</q-btn>
              </q-card-section>

            </q-card>
          </div>
        </q-scroll-area>
        <q-form @submit="onSendQuestion()">
          <q-input
            outlined
            v-model="question_text"
            type="textarea"
            label="Type your message here..."
            :rules="[val => !!val || 'Field is required']"
            />
          <q-btn
            type="submit"
            color="grey-6"
            label="Send"
            size="lg"
            class="full-width q-ma-md">
          </q-btn>

        </q-form>



      </div>
    </div>
  </q-page>
</template>

<script setup>
import { apiAxios } from 'src/boot/axios';
import { date } from "quasar";
import { ref, onMounted } from 'vue';

import { useRouter } from "vue-router";
const router = useRouter();

const question_text = ref("")
const currentCards = ref([]);
const questionCards = ref([])
const data = ref(null);
const currentUserID = ref(null);
const mainScrollArea = ref(null)

//TODO: Make this function scroll to bottom and uncomment calls
function scrollToBottom() {
  const scrollArea = mainScrollArea.value
  const scrollTarget = scrollArea.getScrollTarget()
  const duration = 0 // ms - use 0 to instant scroll
  scrollArea.setScrollPosition('vertical', scrollTarget.scrollHeight, duration);
}

function checkAuth(){
  if (!localStorage.getItem("myString")) {
      router.push("/auth").then(() => {
        window.location.reload();
      });
    }
}
function initiateData() {
  const data = {
    date: date.formatDate(Date.now(), "DD MMM YYYY HH:mm"),
    question:question_text.value
  };
  return data;
}
function checkEmptyCards(){
  return questionCards.value.length === 0
}


function onSendQuestion() {
  getLastCard()
  question_text.value = " "
}

function getCards() {
  return apiAxios.get("/questions").then((response) => {
    data.value  = response.data.data;
    console.log(data.value);
    return data.value;
  });
}


function getLastCard() {
  const data = initiateData()

  apiAxios.get("/users/me/").then((response) => {
    currentUserID.value  = response.data.id;
    console.log(currentUserID.value)
    apiAxios.post(`/users/${currentUserID.value}/items/`, data)
    .then((response) => {
      data.value  = response.data;
      currentCards.value = data.value;
      questionCards.value.push({
        id: currentCards.value["id"],
        date: currentCards.value["date"],
        question: currentCards.value["question"],
        answer: currentCards.value["answer"],
        onClick: () => {
            console.log("Удаляемый объект")
            console.log(currentCards.value["id"])
            apiAxios.delete(`/items/delete/${currentCards.value["id"]}/`)
            questionCards.value.splice(questionCards.value.length-1, 1);
        }
        });
    });
  });



}




function getQuestionCards() {
  apiAxios.get("/users/me/").then((response) => {
    currentUserID.value  = response.data.id;
    console.log(currentUserID.value)
    apiAxios.get(`/users/${currentUserID.value}/items/`)
    .then((response) => {
      currentCards.value = response.data;
      const numCards = currentCards.value.length;

      console.log(currentCards.value);
      console.log(numCards);

      for (let i = 0; i < numCards; i++) {
        questionCards.value.push({
          id: currentCards.value[i]["id"],
          date: currentCards.value[i]["date"],
          question: currentCards.value[i]["question"],
          answer: currentCards.value[i]["answer"],
          onClick: () => {
            console.log("Удаляемый объект")
            console.log(questionCards.value[i]["id"])
            apiAxios.delete(`/items/delete/${questionCards.value[i]["id"]}/`)
            questionCards.value.splice(i, 1);
          }
        });
    }
    });
  });



}

onMounted(() => {
    checkAuth();
    getQuestionCards();
});

</script>

<style lang="scss">
#IndexStyle{
  .scrollStyle{
    height: 60vh;
    width: 100%;
  }



}
</style>
