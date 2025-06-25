<script lang="ts">
import myClock from '../components/myClock.vue'
import { defineComponent } from 'vue'
import { descriptionItemProps, ElMessageBox } from 'element-plus'
import type { Action } from 'element-plus'

export default defineComponent({
  name: 'DataSetManagement',
  inject: ['user'],
  components: { myClock },
  data() {
    return {
      back_end: 'http://127.0.0.1:5000',
      datasets: [] as Array<{ id: number; user_id: number; name: string; description: string; size: number; created_at: string }>,
      stats: { dataset_num: 0, total_size: 0.0 },
      searchKey: '',
      uploadFile: null as File | null,
      datasetName: '',
      datasetDesc: '',
      currentPage: 1,
      pageSize: 6,
      loading: false,
      uploadLoading: false,
      isUploadDialogVisible: false,
      showDescDialog: false,
      descDialogContent: ''
    }
  },
  methods: {
    async getDatasets() {
      try {
        this.loading = true
        const userId = (this.user as any).id
        const url = `${this.back_end}/datasets?search=${encodeURIComponent(this.searchKey)}&page=${this.currentPage}&size=${this.pageSize}`
        const res = await fetch(url)
        const data = await res.json()
        if (!res.ok) throw new Error(data.error || '获取数据失败')

        this.datasets = data.list.map((d: any) => ({
          ...d,
          description: d.description || '-',
          created_at: d.created_at ? new Date(d.created_at).toLocaleString() : '-'
        }))

        this.stats.dataset_num = data.total
        this.stats.total_size = data.total_size || 0

        console.log(this.stats.total_size)
      } catch (err: any) {
        console.error(err)
        this.$message.error(`获取数据失败: ${err.message}`)
      }
      finally {
        this.loading = false
      }
    },
    handleFileChange(file: any) {
      this.uploadFile = file.raw
      if (!this.datasetName) {
        this.datasetName = file.name.split('.').slice(0, -1).join('.')
      }
    },
    async uploadDataset() {
      if (!this.uploadFile) return this.$message.warning('请选择文件')
      if (!this.datasetName) { return this.$message.warning('请输入数据集名称'); }
      this.uploadLoading = true

      const form = new FormData()
      form.append('file', this.uploadFile)
      if (this.datasetName) form.append('name', this.datasetName)
      if (this.datasetDesc) form.append('description', this.datasetDesc)

      try {
        const res = await fetch(`${this.back_end}/datasets`, { method: 'POST', body: form })
        const data = await res.json()
        if (!res.ok) throw new Error(data.error || '上传失败')
        this.$message.success('上传成功')
        this.isUploadDialogVisible = false
        this.resetUploadForm()
        this.getDatasets()
      } catch (err: any) {
        console.error(err)
        this.$message.error(`上传失败: ${err.message}`)
      } finally {
        this.uploadLoading = false
      }
    },
    resetUploadForm() {
      this.uploadFile = null
      this.datasetName = ''
      this.datasetDesc = ''
    },
    confirmDelete(id: number, name: string) {
      ElMessageBox.confirm(
        `确定要删除数据集 "${name}" 吗？此操作不可恢复。`,
        '警告',
        {

          buttonSize: 'large',
          confirmButtonText: '删除',
          cancelButtonText: '取消',
          type: 'warning',
          center: true,
          confirmButtonClass: 'el-button--danger'
        }
      )
        .then(() => {
          this.deleteDataset(id)
        })
        .catch(() => { })
    },
    async deleteDataset(id: number) {
      try {
        const res = await fetch(`${this.back_end}/datasets/${id}`, { method: 'DELETE' })
        if (!res.ok) throw new Error('删除失败')
        this.$message.success('删除成功')
        this.getDatasets()
      } catch (err: any) {
        console.error(err)
        this.$message.error(err.message || '删除失败')
      }
    },
    handlePageChange(page: number) {
      this.currentPage = page
      this.getDatasets()
    },
    formatSize(size: number) {
      if (size < 1024) return `${size.toFixed(2)} MB`
      return `${(size / 1024).toFixed(2)} GB`
    },
    showDesc(desc: string) {
      this.descDialogContent = desc
      this.showDescDialog = true
    }
  },
  mounted() {
    this.getDatasets()
  }
})
</script>

<template>
  <div class="page-container">
    <div class="header">
      <div class="title-group">
        <h1 class="page-title">数据集管理</h1>
      </div>
      <div class="time-container">
        <el-icon :size="20" class="clock-icon">
          <Clock />
        </el-icon>
        <myClock />
      </div>
    </div>

    <div class="dashboard">
      <el-card class="stats-card">
        <div class="stat-item">
          <el-icon class="stat-icon">
            <Folder />
          </el-icon>
          <div>
            <div class="stat-label">数据集数量</div>
            <div class="stat-value">{{ stats.dataset_num }}</div>
          </div>
        </div>
        <div class="stat-item">
          <el-icon class="stat-icon">
            <DataLine />
          </el-icon>
          <div>
            <div class="stat-label">总存储空间</div>
            <div class="stat-value">{{ formatSize(stats.total_size) }}</div>
          </div>
        </div>
      </el-card>

      <el-card class="main-card">
        <div class="toolbar">
          <el-input v-model="searchKey" placeholder="搜索数据集..." clearable class="search-input large-input"
            @input="getDatasets">
            <template #prefix>
              <el-icon>
                <Search />
              </el-icon>
            </template>
          </el-input>

          <el-button type="primary" @click="isUploadDialogVisible = true" class="upload-button large-button">
            <el-icon>
              <Plus />
            </el-icon> 上传数据集
          </el-button>
        </div>

        <el-table :data="datasets" v-loading="loading" stripe :border="true" size="large"
          style="width: 100%;height: 100%; margin-top: 20px; font-size: 18px;" row-class-name="large-row"
          empty-text="暂无数据集">
          <el-table-column prop="name" label="数据集名称" min-width="210" />
          <el-table-column label="大小" width="190">
            <template #default="{ row }">
              {{ formatSize(row.size) }}
            </template>
          </el-table-column>

          <el-table-column label="信息" min-width="190">
            <template #default="{ row }">
              <span class="description-cell">{{ row.description || '-' }}</span>
              <el-link v-if="row.description && row.description.length > 20" type="primary"
                @click="showDesc(row.description)" style="margin-left:8px;">查看全部</el-link>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="210" />
          <el-table-column label="操作" width="100" align="center">
            <template #default="{ row }">
              <el-button type="danger" size="small" plain @click="confirmDelete(row.id, row.name)">
                <el-icon>
                  <Delete />
                </el-icon>
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-pagination class="pagination" background layout="total, prev, pager, next, jumper"
          :current-page="currentPage" :page-size="pageSize" :total="stats.dataset_num" size="large"
          @current-change="handlePageChange" />
      </el-card>
    </div>

    <!-- 上传数据集对话框 -->
    <el-dialog v-model="isUploadDialogVisible" title="上传新数据集" width="500px" @closed="resetUploadForm">
      <el-form label-width="100px" label-position="top">
        <el-form-item label="选择文件" required>
          <el-upload class="upload-area" drag :auto-upload="false" :show-file-list="false"
            :on-change="handleFileChange">
            <div class="upload-content">
              <el-icon class="upload-icon">
                <UploadFilled />
              </el-icon>
              <div class="upload-text">
                <p>拖放文件到此处或点击上传</p>
                <p class="upload-hint">仅支持zip格式文件</p>
              </div>
            </div>
          </el-upload>
          <div v-if="uploadFile" class="file-preview">
            <el-icon>
              <Document />
            </el-icon>
            <span>{{ uploadFile.name }}</span>
            <span class="file-size">({{ formatSize(uploadFile.size / 1024 / 1024) }})</span>
          </div>
        </el-form-item>

        <el-form-item label="数据集名称">
          <!-- 添加字符限制 -->
          <el-input v-model="datasetName" placeholder="请输入数据集名称（必填）" clearable maxlength="15" show-word-limit />
        </el-form-item>

        <el-form-item label="描述信息">
          <!-- 添加字符限制 -->
          <el-input v-model="datasetDesc" type="textarea" placeholder="请输入数据集描述信息（可选）" :rows="3" maxlength="100"
            show-word-limit size="large" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click=" isUploadDialogVisible = false" size="large">取消</el-button>
        <el-button type="primary" @click="uploadDataset" :disabled="!uploadFile || !datasetName"
          :loading="uploadLoading" size="large">
          确认上传
        </el-button>
      </template>
    </el-dialog>

    <!-- 描述信息查看全部对话框 -->
    <el-dialog v-model="showDescDialog" title="详细信息" width="400px" :show-close="true">
      <div style="white-space: pre-wrap;">{{ descDialogContent }}</div>
    </el-dialog>
  </div>
</template>

<style scoped>
.page-container {
  width: 90%;
  height: 100%;
  padding: 20px;
  /* max-width: 1400px; */
  margin: 0 auto;
}

.header {
  display: flex;
  height: 12%;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4edff 100%);
  padding: 20px 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.title-group {
  .page-title {
    font-size: 1.8rem;
    font-weight: 600;
    color: #2c3e50;
    margin: 0 0 8px 0;
  }

  .greeting {
    font-size: 1rem;
    color: #5a6d88;
    margin: 0;
  }
}

.time-container {
  display: flex;
  align-items: center;
  gap: 10px;
  /* background: white; */
  padding: 8px 16px;
  border-radius: 30px;
  /* box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); */

  .clock-icon {
    color: #409eff;
  }
}

.dashboard {
  height: 80%;
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 20px;
}

.stats-card {
  /* height: 100%; */
  /* height: fit-content; */
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: none;

  .stat-item {
    display: flex;
    align-items: center;
    padding: 20px 0;
    border-bottom: 1px solid #eee;

    &:last-child {
      border-bottom: none;
    }
  }

  .stat-icon {
    font-size: 2.2rem;
    margin-right: 15px;
    color: #409eff;
  }

  .stat-label {
    font-size: 0.95rem;
    color: #7a8ca5;
    margin-bottom: 5px;
  }

  .stat-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #2c3e50;
  }
}

.main-card {
  height: auto;
  display: inline-table;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: none;
  padding: 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  gap: 15px;

  .search-input {
    flex: 1;
    max-width: 400px;
  }
}

.upload-area {
  width: 100%;

  :deep(.el-upload) {
    width: 100%;
  }

  :deep(.el-upload-dragger) {
    width: 100%;
    padding: 30px;
    border-radius: 8px;
    border: 1px dashed #409eff;
    background-color: #f8fbff;
    transition: all 0.3s;

    &:hover {
      border-color: #79bbff;
      background-color: #ecf5ff;
    }
  }
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;

  .upload-icon {
    font-size: 50px;
    color: #409eff;
    margin-bottom: 15px;
  }

  .upload-text {
    text-align: center;
    font-size: 15px;
    color: #606266;

    .upload-hint {
      font-size: 12px;
      color: #909399;
      margin-top: 8px;
    }
  }
}

.file-preview {
  display: flex;
  align-items: center;
  margin-top: 15px;
  padding: 10px 15px;
  background-color: #f5f7fa;
  border-radius: 6px;
  font-size: 14px;

  .el-icon {
    margin-right: 8px;
    color: #409eff;
  }

  .file-size {
    margin-left: 8px;
    color: #909399;
  }
}

.pagination {
  margin-top: 25px;
  justify-content: flex-end;
}

.upload-button {
  display: flex;
  align-items: center;

  .el-icon {
    margin-right: 6px;
  }
}

.el-table .el-table__cell {
  font-size: 18px;
  padding: 18px 0;
}

.el-table .large-row {
  height: 60px;
}

.el-table .el-link {
  font-size: 16px;
}

.el-table .description-cell {
  font-size: 16px;
  max-width: 170px;
}

.el-pagination {
  font-size: 17px;
}

.description-cell {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 120px;
  display: inline-block;
  vertical-align: middle;
}

.search-input.large-input {
  font-size: 1vw;
}

.upload-button.large-button {
  height: 2vw;
  width: 15%;
  font-size: 1vw;
}

.el-form-item .el-input {
  font-size: 18px;
  height: 44px;
}

.el-form-item .el-upload {
  font-size: 18px;
}
</style>
