<template>
  <table class="table mail-table">
    <tbody>
      <tr v-for="email in unarchivedEmails"
        :key="email.id"
        :class="['clickable', email.read ? 'read' : '']"
        @click="openEmail(email)"
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
      <tr v-if="openedEmail">
        <td colspan="5">
          <mail-view :email="openedEmail" />
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { format } from 'date-fns';
import { ref } from 'vue';

import { getEmails, updateEmail } from '../services/emailService';
import MailView from './MailView.vue';

export default {
  async setup() {
    const emails = await getEmails();
    return {
      format,
      "emails": ref(emails),
      openedEmail: ref(null)
    };
  },
  components: {
    MailView,
  },
  methods: {
    openEmail(email) {
      email.read = true;
      this.updateEmail(email);
      this.openedEmail = email;
    },
    markEmailArchived(email) {
      email.archived = true;
      this.updateEmail(email);
    },
    updateEmail(email) {
      updateEmail(email.id, email).then(res => {
        console.log(res);
      }).catch(err => {
        console.error(err);
      });
    },
  },
  computed: {
    unarchivedEmails() {
      return this.emails.filter(e => !e.archived);
    },
  }
};
</script>

<style scoped>
  .read {
    opacity: 0.5;
  }
</style>
