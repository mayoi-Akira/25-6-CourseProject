<script lang="ts">
import myClock from '../components/myClock.vue'
export default {
  name: 'DataSetManagement',
  inject: ['user'],
  components: { myClock },
  data() {
    return {
      back_end: 'http://127.0.0.1:5000',
      datasets: [] as Array<{ id: number; name: string; samples: number; size: string; owner: string }>,
      stats: {
        dataset_num: 0,
        total_samples: 0,
        total_size: 0.0,
        avg_samples: 0.0,
      },
      searchKey: '',
      uploadFile: null as File | null,
      currentPage: 1,
      pageSize: 10,
    }
  },
  methods: {
    async getDatasets() {
      try {
        const response = await fetch(`${this.back_end}/datasets?search=${encodeURIComponent(this.searchKey)}&page=${this.currentPage}&size=${this.pageSize}`)
        if (!response.ok) throw new Error(`Failed to fetch datasets: ${response.status}`)
        const data = await response.json()
        this.datasets = data.list
        this.stats = data.stats
      } catch (err) {
        console.error(err)
        this.$message.error('数据集获取失败')
      }
    },
    async uploadDataset() {
      if (!this.uploadFile) return this.$message.warning('请选择文件')
      const form = new FormData()
      form.append('zip_file', this.uploadFile)
      try {
        const response = await fetch(`${this.back_end}/datasets`, { method: 'POST', body: form })
        if (!response.ok) {
          const data = await response.json()
          console.error(response.status)
          throw new Error(`${data.error}`)
        }
        this.$message.success('上传成功')
        this.getDatasets()
      } catch (err) {
        this.$message.error(`${err}`)
      }
    },
    async deleteDataset(id: number) {
      try {
        const response = await fetch(`${this.back_end}/datasets/${id}`, { method: 'DELETE' })
        if (!response.ok) throw new Error(`删除失败 ${response.status}`)
        this.$message.success('删除成功')
        this.getDatasets()
      } catch (err) {
        console.error(err)
        this.$message.error('删除失败')
      }
    },
    handleFileChange(ev: Event) {
      const files = (ev.target as HTMLInputElement).files
      if (files) this.uploadFile = files[0]
    },
    handlePageChange(page: number) {
      this.currentPage = page
      this.getDatasets()
    },
    temp() { }
  },
  mounted() {
    this.getDatasets()
  }
}
</script>

<template>
  <div class="welcome">
    <div style="position:absolute; left:5%; top:50%; transform: translateY(-50%)">
      <i>Hello, {{ user.name }} ~ 数据集管理</i>
    </div>
    <div class="time-container">
      <el-icon style="margin-right: 8px">
        <Clock />
      </el-icon>
      <myClock />
    </div>
  </div>

  <div class="content">
    <div class="sidebar-stats">
      <el-card class="stat-card">
        <p>数据集数量：<strong>{{ stats.dataset_num }}</strong></p>
        <p>总样本数：<strong>{{ stats.total_samples }}</strong></p>
      </el-card>
      <el-card class="stat-card">
        <p>总大小(GB)：<strong>{{ stats.total_size }}</strong></p>
        <p>平均样本数：<strong>{{ stats.avg_samples.toFixed(1) }}</strong></p>
      </el-card>
    </div>

    <div class="main-panel">
      <div class="actions">
        <el-input v-model="searchKey" placeholder="搜索数据集" class="search-input" @keydown.enter.native="getDatasets" />
        <input type="file" @change="handleFileChange" class="file-input" />
        <el-button type="primary" @click="uploadDataset">上传数据集</el-button>
      </div>

      <el-table :data="datasets" stripe style="width: 100%; margin-top: 16px">
        <el-table-column prop="name" label="名称" width="200" />
        <el-table-column prop="samples" label="样本数" width="120" />
        <el-table-column prop="size" label="大小" width="120" />
        <el-table-column prop="owner" label="拥有者" width="150" />
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button type="text" size="small" @click="temp">查看</el-button>
            <el-button type="text" size="small" @click="deleteDataset(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination style="margin-top: 16px; text-align: right" background layout="prev, pager, next"
        :current-page="currentPage" :page-size="pageSize" @current-change="handlePageChange"
        :total="stats.dataset_num" />
    </div>
  </div>
</template>

<style scoped>
.welcome {
  background-color: #ffffff;
  width: 100%;
  height: 60px;
  border-radius: 1.6rem;
  box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.2);
  position: relative;
  padding: 0 20px;
  display: flex;
  align-items: center;
  font-size: 1.2rem;
}

.time-container {
  position: absolute;
  right: 5%;
  display: flex;
  align-items: center;
}

.content {
  display: flex;
  margin-top: 20px;
}

.sidebar-stats {
  width: 25%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stat-card {
  padding: 16px;
  text-align: left;
}

.main-panel {
  width: 75%;
  padding-left: 20px;
}

.actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-input {
  width: 200px;
}

.file-input {
  font-size: 0.9rem;
}
</style>
