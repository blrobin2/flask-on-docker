<template>
  <div class="email-display">
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