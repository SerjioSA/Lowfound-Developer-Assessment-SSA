<template>
  <q-page id="IndexStyle" class="flex flex-center">
    <div class="row full-width full-height q-pa-sm">
      <div class="col">

        <q-scroll-area ref="mainScrollArea" class="scrollStyle q-pb-md">
          <div>
            <q-card  v-for="item in questionCards" :key="item.id" class="cardStyle full-width bg-grey-3 q-ma-sm">

              <q-card-section >
                <div class="text-grey-6 q-py-sm" >{{item.date}}</div>

                <div class="text-blue-6">You asked:</div>
                <p>{{ item.question }}</p>

                <div class="text-blue-6">GPT responded:</div>
                <p>{{ item.answer }}</p>
                <q-btn flat padding="none" class="text-red">Delete</q-btn>
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

const question_text = ref("")
const currentCards = ref([]);
const questionCards = ref([])
const data = ref(null);
const mainScrollArea = ref(null)

//TODO: Make this function scroll to bottom and uncomment calls
function scrollToBottom() {
  const scrollArea = mainScrollArea.value
  const scrollTarget = scrollArea.getScrollTarget()
  const duration = 0 // ms - use 0 to instant scroll
  scrollArea.setScrollPosition('vertical', scrollTarget.scrollHeight, duration);
}


function initiateData() {
  const data = {
    date: date.formatDate(Date.now(), "DD MMM YYYY HH:mm"),
    question:question_text.value
  };
  return data;
}


function onSendQuestion() {
  getLastCard()
  question_text.value = " "
  // window.location.reload();
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
  apiAxios.post("/ask-question", data)
  .then((response) => {
    data.value  = response.data.data;
    currentCards.value = data.value;
    questionCards.value.push({
      id: currentCards.value["id"],
      date: currentCards.value["date"],
      question: currentCards.value["question"],
      answer: currentCards.value["answer"]
      });
  });
}




async function getQuestionCards() {
  const response = await getCards();
  if (response.length > 0){
    currentCards.value = response;
    const numCards = currentCards.value.length;

    console.log(currentCards.value);
    console.log(numCards);

    for (let i = 0; i < numCards; i++) {
      questionCards.value.push({
        id: currentCards.value[i]["id"],
        date: currentCards.value[i]["date"],
        question: currentCards.value[i]["question"],
        answer: currentCards.value[i]["answer"]
      });
    }
}
  // scrollToBottom()
}

onMounted(() => {

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
