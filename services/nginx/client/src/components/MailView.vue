<template>
  <div class="email-display">
    <div class="btn-group" role="button" aria-label="Actions">
      <button type="button" class="btn btn-sm btn-primary" @click="toggleArchive">{{ email.archived ? 'Move to Inbox (e)': 'Archive (e)' }}</button>
      <button type="button" class="btn btn-sm btn-primary" @click="toggleRead">{{ email.read ? 'Mark Unread (r)' : 'Mark Read (r)' }}</button>
      <button type="button" class="btn btn-sm btn-secondary" @click="goNewer">Newer (k)</button>
      <button type="button" class="btn btn-sm btn-secondary" @click="goOlder">Older (j)</button>
    </div>
    <div>
      <em>From {{ email.from_email }} on {{ format(new Date(email.sent_at), 'MMMM do yyyy') }}</em>
    </div>
    <div v-html="marked(email.body)" />
  </div>
</template>

<script>
import { format } from 'date-fns';
import marked from 'marked';

import useKeydown from '../composables/use-keydown';

export default {
  setup(props, { emit }) {
    const toggleRead = () => {
      emit('toggleRead', props.email);
    };

    const toggleArchive = () => {
      emit('toggleArchive', props.email);
    };

    useKeydown([
      { key: 'r', fn: toggleRead },
      { key: 'e', fn: toggleArchive },
    ]);

    return {
      format,
      marked,
      toggleRead,
      toggleArchive,
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