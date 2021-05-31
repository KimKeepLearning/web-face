<template>
  <div>
    <el-row>
      <logo/>
    </el-row>
    <el-row>
      <upload/>
    </el-row>
    <!-- <el-row>
      <show/>
    </el-row> -->
  </div>
</template>

<script>
import Logo from '../components/Logo.vue'
import Upload from '../components/index/upload.vue'
// import Show from '../components/index/showresults.vue'
export default {
  components: {
    Upload,
    Logo,
    // Show
  }
}
</script>

<style>

</style>
