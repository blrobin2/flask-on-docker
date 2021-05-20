<template>
  <div class="container">
    <h1>Inbox</h1>

    <Suspense>
      <template #default>
        <MailTable />
      </template>
      <template #fallback>
        Loading&hellip;
      </template>
    </Suspense>
  </div>
</template>

<script>
  import MailTable from '@/components/MailTable.vue';

  export default {
    name: 'App',
    components: {
      MailTable
    }
  }
</script>
