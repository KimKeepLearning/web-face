import mongoose from 'mongoose'
const Schema = mongoose.Schema

const face_info = new Schema({
  id:{
    type: String,
    require: true,
  },
  path:{
    type:String,
    require:true,
  }
})

export default mongoose.model('face_info', face_info)