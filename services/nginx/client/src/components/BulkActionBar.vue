<template>
  <div>
    <input
      type="checkbox"
      :checked="allEmailsSelected"
      :indeterminate="someEmailsSelected"
      class="form-check-input"
      @click="bulkSelect"
    />
  </div>
</template>

<script>
import { computed } from 'vue';

import useEmailSelection from '@/composables/use-email-selection';

export default {
  setup(props) {
    const emailSelection = useEmailSelection();
    const numberSelected = computed(() => emailSelection.emails.size);
    const allEmailsSelected = computed(() => numberSelected.value === props.emails.length);
    const someEmailsSelected = computed(() => {
      return numberSelected.value > 0 && numberSelected.value < props.emails.length;
    });

    const bulkSelect = () => {
      if (allEmailsSelected.value) {
        emailSelection.clear();
      } else {
        emailSelection.addMultiple(props.emails);
      }
    };

    return {
      allEmailsSelected,
      someEmailsSelected,
      bulkSelect,
    };
  },
  props: {
    emails: {
      type: Array,
      required: true,
    },
  },
};
</script>
