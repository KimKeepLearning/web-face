<template>
  <div class="container">
    <div 
      class="v-waterfall-content" 
      id="v-waterfall">
      <div 
        v-for="(img,idx) in waterfallList"
        class="v-waterfall-item"
        :key="idx"
        :style="{top:img.top+'px',left:img.left+'px',width:waterfallImgWidth+'px', height:img.height}">
          <img :src="img.src" alt="">
      </div>
    </div>
  </div>
</template>

<script>
    export default {
        data(){
            return {
                waterfallList:[],
                waterfallImgWidth:100,
                waterfallImgCol:5,
                waterfallImgRight:10,
                waterfallImgBottom:10,
                waterfallDeviationHeight:[],
                imgList:[
                  require('../../assets/images/1.png'),
                  require('../../assets/images/2.png'),
                  require('../../assets/images/3.png'),
                  require('../../assets/images/5.jpg'),
                  require('../../assets/images/6.png'),
                  require('../../assets/images/7.jpg'),
                  require('E:\\wangxu\\database\\CASIA-WebFace\\CASIA-WebFace\\pt1\\0000145\\017.jpg'),
                  require('E:/wangxu/database/CASIA-WebFace/CASIA-WebFace/pt1/0000121/019.jpg'),
                  require('E:/wangxu/database/CASIA-WebFace/CASIA-WebFace/pt1/0000119/084.jpg'),
                ]
            }
        },
        watch: {
          imgList: function(){
            this.calculationWidth();
          }
        },
        mounted(){
            this.calculationWidth();
            let newimgList
            this.$bus.$on('updateList', data =>{
              newimgList = data
              console.log(newimgList)
            })
            if(newimgList) this.imgList = newimgList
        },
        methods:{
            //计算每个图片的宽度或者是列数
            calculationWidth(){
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

