#!/usr/bin/env node

/**
 * 用于托管文档的小型服务器
 *
 * @author wizardforcel
 * @license SATA
 * @version 2020.918.0
 */

const http = require("http")
const path = require("path")
const fs = require("fs")
const zlib = require('zlib')
const url = require('url')

class SimpleServer {

    constructor(ops={}) {
        this.host = ops.host || 'localhost'
        this.port = ops.port || 3000
        this.root = ops.root || process.cwd()
        this.cors = ops.cors
    }
    
    requestHandlerUnsafe(req, res) {
        var {pathname} = url.parse(req.url)
        var fname = path.join(this.root, pathname)
        
        if(!fs.existsSync(fname)) { 
            this.notFoundHandler(req, res, pathname)
            return
        }
        if(fs.statSync(fname).isDirectory()) {
            fname = path.join(fname, 'index.html')
            if(!fs.existsSync(fname)) { 
                this.notFoundHandler(req, res, pathname)
                return
            }
        }
        if(this.cors)
            res.setHeader('Access-Control-Allow-Origin', '*')
        var mineTypeMap = {
            html: 'text/html;charset=utf-8',
            htm: 'text/html;charset=utf-8',
            xml: "text/xml;charset=utf-8",
            png: "image/png",
            jpg: "image/jpeg",
            jpeg: "image/jpeg",
            gif: "image/gif",
            css: "text/css;charset=utf-8",
            txt: "text/plain;charset=utf-8",
            mp3: "audio/mpeg",
            mp4: "video/mp4",
            ico: "image/x-icon",
            tif: "image/tiff",
            svg: "image/svg+xml",
            zip: "application/zip",
            ttf: "font/ttf",
            woff: "font/woff",
            woff2: "font/woff2",
        }
        const extName = path.extname(fname).substr(1)
        if (mineTypeMap[extName]) {
            res.setHeader('Content-Type', mineTypeMap[extName])
        }
        var stream = fs.createReadStream(fname)
        if(req.headers["accept-encoding"] &&
           req.headers["accept-encoding"].includes("gzip") && 
           ['html', 'js', 'css'].includes(extName)) {
             res.setHeader('Content-Encoding', "gzip")
             const gzip = zlib.createGzip()
             stream = stream.pipe(gzip)
        }
        stream.pipe(res)
    }
    
    requestHandler(req, res) {
        try {
            this.requestHandlerUnsafe(req, res)
        } catch(ex) {
            this.errorHandler(req, res, ex)
        }
    }
    
    notFoundHandler(req, res, fname) {
        res.writeHead(404)
        res.end(`${fname} NOT FOUND`)
    }
    
    errorHandler(req, res, err) {
        res.writeHead(500)
        res.end(`INTERNAL SERVER ERROR: ${err}`)
    }
    
    start() {
        var server = http.createServer(this.requestHandler.bind(this))
        server.listen(this.port, this.host,
            () => console.log(`server started on http://${this.host}:${this.port}`))
    }

}

function main() {
    var port = process.argv[2]
    new SimpleServer({
            root: path.join(__dirname, 'doc'),
            port: port
    }).start()
}

if(require.main === module) main()