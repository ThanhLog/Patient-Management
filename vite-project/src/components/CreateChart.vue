<template>
  <div>
    <div class=" w-full top-0 left-0 border-b-2 pb-1">
      <h1 class=" text-2xl font-semibold text-center">Quản lý bệnh nhân</h1>


      <div class="px-3 mt-5 flex gap-3">
        <div class=" w-[70%]">
          <div class=" flex gap-2 w-full">
            <!-- Chọn khoa -->
            <div class=" w-[60%]">
              <select class=" w-full px-2 py-1 bg-slate-800 text-white text-center" v-model="selectedDepartment"
                @change="onDepartmentChange">
                <option class=" font-semibold text-white z-10" value="" disabled selected> -- Chọn khoa -- </option>
                <option v-for="department in departments" :key="department.name" :value="department.name">
                  {{ department.name }}
                </option>
              </select>
            </div>
            <!-- Chọn bênh -->
            <div class=" w-[40%]">
              <select class=" w-full px-2 py-1 bg-slate-800 text-white text-center" v-model="selectDisease">
                <option value="" disabled selected> -- Chọn bệnh -- </option>
                <option v-for="disease in availableDiseases" :key="disease" :value="disease">
                  {{ disease }}
                </option>
              </select>
            </div>
          </div>

          <div class=" mt-3 flex gap-3 items-end">
            <div>
              <div>
                <select class=" bg-slate-600 px-1 py-2 w-full text-white" v-model="selectChart">
                  <option value="" disabled selected> -- Chọn biểu đồ -- </option>
                  <option value="bar">Biểu đồ cột</option>
                  <option value="pie">Biểu đồ tròn</option>
                  <option value="line">Biểu đồ đường</option>
                </select>
              </div>
              <div class=" mt-3 flex gap-3">
                <button @click="selectOption('age_distribution')"
                  class=" bg-gray-600 px-4 py-2 text-white font-semibold text-[12px] rounded-2xl">Phân bố độ
                  tuổi</button>
                <button @click="selectOption('treatment_cost')"
                  class=" bg-gray-600 px-4 py-2 text-white font-semibold text-[12px] rounded-2xl">Chi phí khám chữa
                  bệnh</button>
              </div>

            </div>
            <button @click="selectOption('bed_capacity')"
              class=" h-1/2 bg-gray-600 px-4 py-2 text-white font-semibold text-[12px] rounded-2xl">Công suất giường
              bệnh</button>
            <button @click="selectOption('disease_ratio')"
              class=" h-1/2 bg-gray-600 px-4 py-2 text-white font-semibold text-[12px] rounded-2xl">Tỉ lệ mắc
              bệnh</button>
          </div>
        </div>
        <div class=" w-[30%] bg-white border-2">
          <h2 class=" font-semibold text-[20px] px-2">Review</h2>
          <div class=" p-2 mt-3">
            <p>Khoa: {{ selectedDepartment }}</p>
            <p>Bệnh: {{ selectDisease }}</p>
            <p>Biểu đồ: {{ displayChart }}</p>
            <p>Lựa chọn: {{ displayOptions }}</p>
          </div>

          <div class="flex gap-2 p-2">
            <button @click="resetData" class="w-full bg-red-500 p-2 font-semibold text-white text-[20px]">Xóa</button>
            <button @click="onSubmit" class=" w-full p-2 bg-lime-500 font-semibold text-white text-[20px]">Xác
              nhận</button>
          </div>
        </div>
      </div>
    </div>

    <div class=" bg-white flex">
      <div class=" relative w-[70%]">
        <select v-if="isBedCapacitySelected" v-model="selectedTimeRange" class=" absolute top-0 right-0 m-3"
          @change="fetchBedOccupancy">
          <option value="1_Week" selected>1 Tuần</option>
          <option value="1_Month">1 Tháng</option>
          <option value="3_Month">3 Tháng</option>
          <option value="6_Month">6 Tháng</option>
        </select>
        <img v-if="chartImage" :src="chartImage" alt="">
      </div>

      <!-- List bệnh nhân -->
      <div class=" w-[30%] border-l-2">
        <h1 class=" text-4xl p-2 text-center font-semibold">Danh sách bệnh nhân </h1>

        <div class="h-screen overflow-y-auto">
          <div class=" m-2 p-2 border-2" v-for="item in listPatients" :key="item.name">
            <p>Họ tên: {{ item.name }}</p>
            <p>Giới tính: {{ item.sex }}</p>
            <p>Tuổi: {{ item.age }}</p>
            <p>Bệnh: {{ item.disease }}</p>
            <p>Khoa: {{ item.department }}</p>
            <p>Ngày nhập viện: {{ item.admission_date }}</p>
            <p>Ngày ra viện: {{ item.discharge_date }}</p>
            <p>Chi phí: {{ item.treatment_cost }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from './../api'
export default {
  name: 'MenuVue',
  data() {
    return {
      departments: [], // Danh sách khoa
      availableDiseases: [], // Danh sách bệnh đã chọn theo khoa
      listPatients: [],
      selectedDepartment: "", // Khoa đã chọn
      selectDisease: "", // Bệnh đã chọn
      selectChart: "",
      chartImage: null,
      selectedOption: null,
      selectedTimeRange: "1_Week",

      // Biến để theo dõi các lựa chọn của người dùng
      isAgeDistributionSelected: false,
      isMedicalCostSelected: false,
      isBedCapacitySelected: false,
      isDiseaseRatioSelected: false,

      chartData: null,
      timeRange: "1_Week"
    }
  },

  computed: {
    displayChart() {
      if (this.selectChart == 'bar') {
        return 'Biểu đồ cột'
      }
      else if (this.selectChart == 'pie') {
        return 'Biểu đồ tròn'
      }
      else if (this.selectChart == 'line') {
        return 'Biểu đồ đường'
      }
    },

    displayOptions() {
      if (this.isAgeDistributionSelected) {
        return 'Phân bố độ tuổi';
      }

      if (this.isMedicalCostSelected) {
        return 'Chi phí khám chữa bệnh';
      }

      if (this.isBedCapacitySelected) {
        return 'Công suất giường bệnh';
      }

      if (this.isDiseaseRatioSelected) {
        return 'Tỷ lệ mắc bệnh';
      }
    }
  },

  mounted() {
    this.fetchDepartments()
  },

  methods: {
    // Phương thức gọi API để lấy danh sách khoa
    fetchDepartments() {
      api.getDepartments()
        .then(response => {
          this.departments = response.data;
        })
        .catch(error => {
          console.error('Có lỗi khi gọi API:', error);
        });
    },

    fetchBedOccupancy() {
      const requestData = {
        chart_type: 'line',
        time_range: this.selectedTimeRange,
        // Các tham số khác nếu cần
      };

      api.getBedOccupancy(requestData)
        .then(response => {
          const base64Image = btoa(
            new Uint8Array(response.data).reduce((data, byte) => data + String.fromCharCode(byte), '')
          );

          this.chartImage = `data:image/png;base64,${base64Image}`;
          console.log("Dữ liệu công suất giường bệnh đã được tải thành công:", response.data);
        })
        .catch(error => {
          console.error("Lỗi khi lấy dữ liệu công suất giường bệnh:", error);
        });
    },

    // Phương thức xử lý chọn khoa
    onDepartmentChange() {
      const department = this.departments.find(dep => dep.name === this.selectedDepartment)
      this.availableDiseases = department ? department.responsible_diseases : [];
      this.selectDisease = ""; // Reset bệnh đã chọn
    },

    selectOption(option) {
      this.selectedOption = option

      // Xác định loại biểu đồ đã chọn
      this.isAgeDistributionSelected = (option === 'age_distribution');
      this.isMedicalCostSelected = (option === 'treatment_cost');
      this.isBedCapacitySelected = (option === 'bed_capacity');
      this.isDiseaseRatioSelected = (option === 'disease_ratio')
    },
    resetData() {
      this.selectedDepartment = '';
      this.selectChart = ""
      this.selectDisease = ""
      this.selectedOption = ""
      this.isAgeDistributionSelected = false
      this.isMedicalCostSelected = false
      this.isBedCapacitySelected = false
    },
    onSubmit() {
      const requestData = {
        chart_type: this.selectChart,
        data_type: this.selectedOption, // Kiểm tra data_type (age_distribution, treatment_cost, hoặc bed_capacity)
      };
      // Kiểm tra các điều kiện để thêm giá trị vào requestData
      if (this.selectedDepartment) {
        requestData.department_name = this.selectedDepartment;
      }

      if (this.selectDisease) {
        requestData.disease_name = this.selectDisease;
      }

      console.log(requestData)
      // Xử lý tùy chọn biểu đồ hoặc chi phí khám chữa bệnh
      if (this.selectedOption === 'age_distribution') {
        api.getChartData(requestData)
          .then(response => {
            if (response.data) {
              const reader = new FileReader();
              reader.readAsDataURL(response.data); // Đọc file ảnh trả về từ API
              reader.onloadend = () => {
                this.chartImage = reader.result; // Chuyển đổi sang base64
                this.renderChart(); // Vẽ biểu đồ
                console.log("Dữ liệu biểu đồ đã được tải thành công:", this.chartImage);
              };
            } else {
              console.error("Không nhận được dữ liệu biểu đồ từ API.");
            }
          })
          .catch(error => {
            console.error("Lỗi khi lấy dữ liệu biểu đồ:", error);
          });

      } else if (this.selectedOption === 'bed_capacity') {
        // Thêm khoảng thời gian nếu chọn công suất giường bệnh
        requestData.time_range = this.selectedTimeRange // Giá trị mặc định là 1 tuần
        requestData.chart_type = 'line'


        api.getBedOccupancy(requestData)
          .then(response => {
            if (response.data) {
              // Chuyển đổi dữ liệu thành base64
              const base64Image = btoa(
                new Uint8Array(response.data).reduce((data, byte) => data + String.fromCharCode(byte), '')
              );
              this.chartImage = `data:image/png;base64,${base64Image}`; // Gán chuỗi base64 vào chartImage
              console.log("Dữ liệu công suất giường bệnh đã được tải thành công:", response.data);
            } else {
              console.error("Không nhận được dữ liệu công suất giường bệnh từ API.");
            }
          })
          .catch(error => {
            console.error("Lỗi khi lấy dữ liệu công suất giường bệnh:", error);
          });
      } else if (this.selectedOption === "disease_ratio") {
        api.getDiseaseRatio(requestData).then(
          response => {
            if (response.data) {
              const reader = new FileReader();
              reader.readAsDataURL(response.data); // Đọc file ảnh trả về từ API
              reader.onloadend = () => {
                this.chartImage = reader.result; // Chuyển đổi sang base64
                this.renderChart(); // Vẽ biểu đồ
                console.log("Dữ liệu tỷ lệ bệnh đã được tải thành công:", this.chartImage);
              };
            } else {
              console.error("Không nhận được dữ liệu tỷ lệ bệnh từ API.");
            }
          }
        ).catch(e => {
          console.error("Lỗi khi lấy dữ liệu tỷ lệ bệnh:", e);
        })
      } else if (this.selectedOption === "treatment_cost") {
        api.getTreamentCost(requestData)
          .then(response => {
            if (response.data) {
              const reader = new FileReader();
              reader.readAsDataURL(response.data); // Đọc file ảnh trả về từ API
              reader.onloadend = () => {
                this.chartImage = reader.result; // Chuyển đổi sang base64
                this.renderChart(); // Vẽ biểu đồ
                console.log("Dữ liệu biểu đồ đã được tải thành công:", this.chartImage);
              };
            } else {
              console.error("Không nhận được dữ liệu biểu đồ từ API.");
            }
          })
          .catch(error => {
            console.error("Lỗi khi lấy dữ liệu biểu đồ:", error);
          });

      }
      else {
        console.warn("Tùy chọn không hợp lệ. Vui lòng chọn biểu đồ phù hợp.");
        alert("Vui lòng chọn loại dữ liệu hợp lệ để hiển thị.");
      }

      api.getPatients(requestData).then(response => {
        this.listPatients = response.data
        console.log(response.data)
      }).catch((e) => {
        console.log(e)
      })
    },

    renderChart() {
      const canvas = this.$refs.myChart; // Giả định bạn có một thẻ <canvas> trong template
      const ctx = canvas.getContext('2d');

      // Xóa biểu đồ cũ nếu có
      if (this.chartInstance) {
        this.chartInstance.destroy();
      }

      // Kiểm tra nếu có ảnh biểu đồ
      if (this.chartImage) {
        const img = new Image();
        img.src = this.chartImage;
        img.onload = () => {
          ctx.clearRect(0, 0, canvas.width, canvas.height); // Xóa canvas cũ
          ctx.drawImage(img, 0, 0); // Vẽ ảnh từ base64
        };
      } else {
        console.error("Không có dữ liệu ảnh để hiển thị biểu đồ.");
      }
    },

    onTimeRangeChange(newTimeRange) {
      this.timeRange = newTimeRange
    }
  }
}
</script>
