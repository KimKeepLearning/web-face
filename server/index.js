
const Koa = require('koa')
const consola = require('consola')
const { Nuxt, Builder } = require('nuxt-edge')
const serve = require('koa-static');

const path = require('path');

import mongoose from 'mongoose'
import dbConfig from './dbs/config'
import upload from './interface/upload'

const app = new Koa()
const host = process.env.HOST || '127.0.0.1'
const port = process.env.PORT || 3000

const staticDirPath = path.join(__dirname, '../static');
console.log(staticDirPath)
app.use(serve(staticDirPath))
// app.use(staticFiles(path.join(__dirname , 'static')))

// mongoose配置
mongoose.connect(dbConfig.dbs, {
  useNewUrlParser: true
})

// Import and Set Nuxt.js options
let config = require('../nuxt.config.js')
config.dev = !(app.env === 'production')

async function start() {
  // Instantiate nuxt.js
  const nuxt = new Nuxt(config)

  // Build in development
  if (config.dev) {
    const builder = new Builder(nuxt)
    await builder.build()
  }
  // 自定义的接口
  app.use(upload.routes()).use(upload.allowedMethods())
  
  app.use(ctx => {
    ctx.status = 200 // koa defaults to 404 when it sees that status is unset

    return new Promise((resolve, reject) => {
      ctx.res.on('close', resolve)
      ctx.res.on('finish', resolve)
      nuxt.render(ctx.req, ctx.res, promise => {
        // nuxt.render passes a rejected promise into callback on error.
        promise.then(resolve).catch(reject)
      })
    })
  })

  app.listen(port, host)
  consola.ready({
    message: `Server listening on http://${host}:${port}`,
    badge: true
  })
}

start()
