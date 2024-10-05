<template>
  <div class=" fixed w-full top-0 left-0 border-b-2 pb-1">
    <h1 class=" text-2xl font-semibold text-center">Quản lý bệnh nhân</h1>
    <ul class=" flex justify-around">
      <li v-for="(department, i) in departments" :key="department.name" class="relative group px-2 w-full"
        :class="i % 2 === 0 ? 'bg-slate-400' : 'bg-slate-300'">
        <p class=" text-xl font-semibold">{{ department.name }}</p>
        <ul class="absolute w-full top-[100] left-0 hidden group-hover:block">
          <li v-for="(disease, i) in department.responsible_diseases" :key="disease"
            :class="i % 2 === 0 ? 'bg-slate-100' : 'bg-slate-200'">
            <p class=" px-2 pt-1">{{ disease }}</p>
          </li>
        </ul>
      </li>
    </ul>
    <ul class=" flex gap-2 mt-3 px-2">
      <li class=" bg-slate-400">
        <p class=" px-2 text-slate-100 font-semibold">Độ tuổi</p>
      </li>
      <li class=" bg-slate-400">
        <p class=" px-2 text-slate-100 font-semibold">Công suất giường bệnh</p>
      </li>
    </ul>
  </div>
</template>

<script>
import api from './../api'
export default {
  name: 'MenuVue',
  data() {
    return {
      departments: [],
    }
  },

  mounted() {
    api.getDepartments()
      .then(response => {
        this.departments = response.data;
      })
      .catch(error => {
        console.error('Có lỗi khi gọi API:', error);
      });
  },
}
</script>

<style></style>