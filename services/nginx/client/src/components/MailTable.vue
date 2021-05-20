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
    </tbody>
  </table>
  <modal-view @closeModal="closeEmail" :ref="setModal" v-if="openedEmail">
    <template v-slot:header>
      <h2 class="mb-0">Subject: <strong>{{ openedEmail.subject }}</strong></h2>
    </template>
    <template v-slot:default>
      <mail-view :email="openedEmail" @changeEmail="changeEmail" />
    </template>
  </modal-view>
</template>

<script>
import { Modal } from 'bootstrap';
import { format } from 'date-fns';
import { ref } from 'vue';

import { getEmails, updateEmail } from '../services/emailService';
import MailView from './MailView.vue';
import ModalView from './ModalView.vue';

export default {
  async setup() {
    let modal = null;
    const setModal = el => {
      if (el) {
        modal = new Modal(el.$el);
        modal.show();
      }
    };
    const closeModal = () => {
      modal.hide();
      modal = null;
    };

    const emails = await getEmails();
    return {
      format,
      setModal,
      closeModal,
      "emails": ref(emails),
      openedEmail: ref(null)
    };
  },
  components: {
    MailView,
    ModalView,
  },
  methods: {
    openEmail(email) {
      email.read = true;
      this.updateEmail(email);
      this.openedEmail = email;
    },
    closeEmail() {
      this.closeModal();
      this.openedEmail = null;
    },
    markEmailArchived(email) {
      email.archived = true;
      this.updateEmail(email);
    },
    changeEmail({
      toggleRead,
      toggleArchive,
      save,
      closeModal,
      changeIndex
    }) {
      const email = this.openedEmail;
      if (toggleRead) { email.read = !email.read; }
      if (toggleArchive) { email.archive = !email.archive; }
      if (save) { this.updateEmail(email); }
      if (changeIndex) {
        const emails = this.unarchivedEmails;
        const currentIndex = emails.indexOf(this.openedEmail);
        let newIndex = currentIndex + changeIndex;
        if (newIndex > emails.length - 1) {
          newIndex = 0;
        }
        if (newIndex < 0) {
          newIndex = emails.length - 1;
        }
        const newEmail = emails[newIndex];
        this.openEmail(newEmail);
      }
      if (closeModal) {
        this.closeEmail();
      }
    },
    updateEmail(email) {
      updateEmail(email.id, email).catch(err => {
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
  .clickable {
    cursor: pointer;
  }
  .read {
    opacity: 0.5;
  }
</style>
