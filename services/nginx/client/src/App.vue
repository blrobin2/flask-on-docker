<template>
  <div class="container">
    <h1>Inbox</h1>
    <table class="table mail-table">
      <tbody>
        <tr v-for="email in unarchivedEmails"
          :key="email.id"
          :class="['clickable', email.read ? 'read' : '']"
          @click="markEmailRead(email)"
        >
          <td scope="row"><input type="checkbox" /></td>
          <td>{{ email.from_email }}</td>
          <td class="overflow-hidden">
            <p><strong>{{ email.subject }}</strong> - {{ email.body }}</p>
          </td>
          <td class="date">
            {{ format(new Date(email.sent_at), 'MMMM do yyyy') }}
          </td>
          <td>
            <button class="btn btn-sm btn-info" @click="markEmailArchived(email)">Archive</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { format } from 'date-fns';

import { getEmails } from './services/emailService';

export default {
  data() {
    return {
      format,
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
    markEmailRead(email) {
      email.read = true;
      // updateEmail(email.id, {
      //   read: true
      // }).then(res => {
      //   console.log(res);
      //   this.getEmails();
      // }).catch(err => {
      //   console.error(err);
      // });
    },
    markEmailArchived(email) {
      email.archived = true;
    },
  },
  computed: {
    unarchivedEmails() {
      return this.emails.filter(e => !e.archived);
    },
  },
  mounted() {
    this.getEmails();
  },
};
</script>

<style scoped>
  .read {
    opacity: 0.5;
  }
</style>
