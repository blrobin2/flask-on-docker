<template>
  <div class="email-display">
    <h2 class="mb-0">Subject: <strong>{{ email.subject }}</strong></h2>
    <div>
      <em>From {{ email.from_email }} on {{ format(new Date(email.sent_at), 'MMMM do yyyy') }}</em>
    </div>
    <div v-html="marked(email.body)" />
  </div>
</template>

<script>
import { format } from 'date-fns';
import marked from 'marked';

export default {
  setup() {
    return {
      format,
      marked,
    };
  },
  props: {
    email: {
      type: Object,
      required: true,
    },
  },
};
</script>