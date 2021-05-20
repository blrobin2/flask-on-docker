<template>
  <bulk-action-bar :emails="unarchivedEmails" />
  <table class="table mail-table">
    <tbody>
      <tr v-for="email in unarchivedEmails"
        :key="email.id"
        :class="['clickable', email.read ? 'read' : '']"
      >
        <td scope="row">
          <input type="checkbox"
            @click="emailSelection.toggle(email)"
            :checked="emailSelection.emails.has(email)"
            class="form-check-input"
          />
        </td>
        <td @click="openEmail(email)">{{ email.from_email }}</td>
        <td @click="openEmail(email)">
          <p><strong>{{ email.subject }}</strong> - {{ bodySubstring(email) }}</p>
        </td>
        <td class="date" @click="openEmail(email)">
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

import { getEmails, updateEmail } from '@/services/emailService';
import useEmailSelection from '@/composables/use-email-selection';
import BulkActionBar from '@/components/BulkActionBar.vue';
import MailView from '@/components/MailView.vue';
import ModalView from '@/components/ModalView.vue';

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
      emailSelection: useEmailSelection(),
      format,
      setModal,
      closeModal,
      "emails": ref(emails),
      openedEmail: ref(null)
    };
  },
  components: {
    BulkActionBar,
    MailView,
    ModalView,
  },
  methods: {
    bodySubstring(email) {
      const body = email.body.substring(0, 100 - email.subject.length);
      if (body.length < email.body.length) {
        return body + "\u2026";
      }
      return body;
    },
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
