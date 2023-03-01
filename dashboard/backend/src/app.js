const express = require('express')
const { queryDb } = require('./services/db')
const app = express()
const port = 54321

app.get('/api/applications', (req, res) => {
    const query = queryDb('cpu_gauge')
    res.send(query)
})

app.listen(port, () => {
    console.log(`Dashboard backend listening on port ${port}`)
})