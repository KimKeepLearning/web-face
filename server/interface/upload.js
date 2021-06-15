import Router from 'koa-router'
import axios from './utils/axios'
import {PythonShell} from 'python-shell'
import face_info from '../dbs/models/face_info'
import child_process from 'child_process'
import util from 'util'
import path from 'path'
let router = new Router({
  prefix: '/upload'
})

router.get('/test', async (ctx)=>{

  const filename = ctx.query.filename
  var filePath = path.join('E:/2-JOB/联想小新/简历项目2/web-face/static/images',filename);

  /** child_process 版本 */
  try {
    let now = new Date().getTime()
    let searchResStdout = child_process.execSync('python E:/2-JOB/联想小新/简历项目2/web-face/server/interface/python-file/test.py ' + filePath);
    console.log('consuming: ', new Date().getTime() - now)
    let searchLabels = searchResStdout.toString('utf8')
    searchLabels = searchLabels.slice(1, searchLabels.length - 1).split(' ').map((item)=> parseInt(item)).filter(item=>!isNaN(item));


    let paths = [];
    for(let id of searchLabels){
      // console.log(id)
      paths.push(await face_info.findOne({
        id
      }))
    }
    // console.log(paths)
    ctx.body = {
      msg:' 后端返回',
      data: paths.map(item=>item.path)
    }
  } catch (e) {
    ctx.body = {
      msg:' 后端返回',
      data: []
    }
  }
})


export default router;