<template>
  <h1>Inbox</h1>
</template>

<script>
import { getEmails } from './services/emailService';

export default {
  data() {
    return {
      emails: [],
    };
  },
  methods: {
    getEmails() {
      getEmails()
        .then(res => {
          console.log(res);
          this.emails = res.items;
        })
        .catch(err => {
          console.error(err);
        });
    },
  },
  mounted() {
    this.getEmails();
  },
};
</script>