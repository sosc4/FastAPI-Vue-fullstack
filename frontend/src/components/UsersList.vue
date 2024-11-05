<script lang="ts" setup>
  import { UserResponse } from '@/interfaces'
  import { defineEmits, defineProps } from 'vue'

  const props = defineProps<{
    users: UserResponse[]
  }>()

  const emit = defineEmits<{
    (e: 'delete', id: number): void
    (e: 'ban', id: number): void
    (e: 'unban', id: number): void
    (e: 'edit', id: number): void
  }>()

  const handleDelete = (id: number) => emit('delete', id)
  const handleBan = (id: number) => emit('ban', id)
  const handleEdit = (id: number) => emit('edit', id)
  const handleUnban = (id: number) => emit('unban', id)
</script>

<template>
  <v-table>
    <thead>
      <tr>
        <th
          v-for="header in [
            'ID', 'Nazwa użytkownika', 'Administrator?', 'Zbanowany?', 'Akcje'
          ]"
        >
          {{ header }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="user in props.users"
        :key="user.id"
      >
        <td>
          {{ user.id }}
        </td>
        <td>
          {{ user.username }}
        </td>
        <td>
          <v-icon v-if="user.is_admin" color="primary" icon="mdi-check" />
        </td>
        <td>
          <v-icon v-if="!user.is_active" color="error" icon="mdi-check" />
        </td>
        <td>
          <v-btn
            v-if="!user.is_admin"
            class="mr-2"
            icon="mdi-pencil"
            variant="plain"
            @click="handleEdit(user.id)"
          />

          <v-btn
            v-if="!user.is_admin"
            class="mr-2"
            icon="mdi-delete"
            variant="plain"
            @click="handleDelete(user.id)"
          />

          <v-btn
            v-if="!user.is_admin"
            variant="plain"
            @click="user.is_active ? handleBan(user.id) : handleUnban(user.id)"
          >
            {{ user.is_active ? 'Zbanuj' : 'Odbanuj' }}
          </v-btn>

        </td>
      </tr>
    </tbody>
  </v-table>
</template>

<style lang="scss" scoped>
/* No custom styles as per the request */
</style>
