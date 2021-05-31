<template>
  <el-row class="container">
    <!--上传-->
    <el-upload
      class="upload"
      drag
      accept="image/jpeg,image/gif,image/png"
      :action="action"
      :file-list="uploadList"
      :http-request="handleGetImage"
      v-if="!uploadList.length"
      >
    <i class="el-icon-upload"></i>
    <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
    </el-upload>
    <div
      v-else
      class="showSmall">
      <img 
        :src="displayImage" 
        alt=""
      >
    </div>
    <!--开始搜索，触发事件-->
    <el-button 
      class="btn"
      :disabled="!uploadList.length"
      @click="handleUpload"
      >开始搜索</el-button>
    <!--显示区域-->
    <div 
      class="v-waterfall-content" 
      id="v-waterfall"
      >
      <div v-if="res_is_show">
        <div 
          v-for="(img,idx) in waterfallList"
          class="v-waterfall-item"
          :key="idx"
          :style="{top:img.top+'px',left:img.left+'px',width:waterfallImgWidth+'px', height:img.height}">
            <img :src="img.src" alt="">
        </div>
      </div>
    </div>
    
  </el-row>
</template>

<script>


export default {
  // 难点，v-for无法实现数据的双向绑定
  data () {
    return {
      action: "",
      uploadList: [],
      waterfallList:[],
      waterfallImgWidth:100,
      waterfallImgCol:5,
      waterfallImgRight:10,
      waterfallImgBottom:10,
      waterfallDeviationHeight:[],
      res_is_show: true,
      imgList:[
        require('../../assets/images/1.png'),
        require('../../assets/images/2.png'),
        require('../../assets/images/3.png'),
        require('../../assets/images/5.jpg'),
        require('../../assets/images/6.png'),
        require('../../assets/images/7.jpg'),
        require('../../assets/images/7.jpg'),
        require('../../assets/images/7.jpg'),
        require('../../assets/images/7.jpg'),
      ]
    }
  },
  computed: {
    displayImage () {
      return 'images/' + this.uploadList[this.uploadList.length - 1].name
    }
  },
  watch:{
    imgList(){
      this.res_is_show = false
      
      if(true){
        this.$nextTick(()=>{
          
          this.calculationWidth();
          this.res_is_show = true
          
        })
      }
    }
  },
  mounted(){
    this.calculationWidth();
  },
  methods:{
    handleGetImage (req) {
      // console.log(req)
      let filename = req.file.name
      let id = req.file.uid
      this.uploadList.push({
        name:filename,
        id:id,
      })
    },
    async handleUpload (){
      // console.log(this.uploadList)
      let self = this
      let uploadData = this.uploadList[this.uploadList.length - 1]
      let {status, data} = await self.$axios.get('/upload/test',{
        params:{
          filename: uploadData.name,
          id: uploadData.id
        }
      })
      if(status === 200 && data.data){
        // console.log('后端返回的数据:', data)

        // this.imgList = data.data.map(item=>item.split('\\')[7] + '/' + item.split('\\')[8] + '/' +item.split('\\')[9])
        this.imgList = data.data.map(item=> item.split('casia')[1])
        for(let i = 0, n = this.imgList.length; i<20;i++){
         
          // this.imgList[i] = '../../static/images/' + this.imgList[i]
          // this.imgList[i] = require('E:/2-JOB/联想小新/简历项目2/casia' + this.imgList[i])
          this.imgList[i] = '/casia' + this.imgList[i]
        }
        // console.log(this.imgList)
      } else {
        alert('最好选择正脸清晰照哦')
        this.$router.go(0)
      }
      
    },
    calculationWidth(){
      // console.log('!!!!!')
      let domWidth = document.getElementById("v-waterfall").offsetWidth;
      // 如果图片目标宽度不存在或者瀑布流的列数不存在的话
      if (!this.waterfallImgWidth && this.waterfallImgCol){
          this.waterfallImgWidth = (domWidth-this.waterfallImgRight*this.waterfallImgCol)/this.waterfallImgCol;
      }else if(this.waterfallImgWidth && !this.waterfallImgCol){
          this.waterfallImgCol = Math.floor(domWidth/(this.waterfallImgWidth+this.waterfallImgRight))
      }
      //初始化偏移高度数组
      this.waterfallDeviationHeight = new Array(this.waterfallImgCol);
      for (let i = 0, len = this.waterfallDeviationHeight.length;i < len;i++){
          this.waterfallDeviationHeight[i] = 0; // 每列的高度初始化为0
      }
      this.imgPreloading()
    },
    //图片预加载
    imgPreloading(){
      // console.log(this.imgList)
      this.waterfallList = []
      for (let i = 0;i < this.imgList.length;i++){
        let aImg = new Image();
        aImg.src = this.imgList[i];
        aImg.onload = aImg.onerror = (e)=>{
          let imgData = {};
          imgData.height = this.waterfallImgWidth/aImg.width*aImg.height; // 根据图片的比例，计算缩放后的高度
          imgData.src = this.imgList[i];
          this.waterfallList.push(imgData);
          this.rankImg(imgData); // 给图片安排合适的位置
        }
      }
    },
    //瀑布流布局
    rankImg(imgData){
        let {waterfallImgWidth,waterfallImgRight,waterfallImgBottom,waterfallDeviationHeight,waterfallImgCol} = this;
      
        let minIndex = this.filterMin(); // 目前高度最小的列
        imgData.top = waterfallDeviationHeight[ minIndex ]; // 图像top=该列累计的高度
        imgData.left = minIndex * (waterfallImgRight + waterfallImgWidth); // 图像left=列的位置 * (每个图像宽度 + margin-left)
        waterfallDeviationHeight[minIndex] += imgData.height + waterfallImgBottom; // 更新高度数组
        
    },
    /**
     * 找到最短的列并返回下标
     * @returns {number} 下标
     */
    filterMin(){
        const min = Math.min.apply(null, this.waterfallDeviationHeight);
        return this.waterfallDeviationHeight.indexOf(min);
    }
  }
}
</script>

<style lang='scss'>
@import "/assets/css/global.scss";
@import "/assets/css/index/upload.scss";

.v-waterfall-content{
  width: 540px;
  position: relative;
  margin: 0 auto;
  .v-waterfall-item{
    position: absolute;
    img{
      width: 100%;
      height: 100%;
    }
  }
}

</style>
