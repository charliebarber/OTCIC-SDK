const axios = require('axios')

const PROM_URL = 'http://prometheus:9090/api/v1/'

const queryDb = (query) => {
    axios.get(PROM_URL + 'query?query=' + query)
        .then((res) => {
            console.log(res)
            return res
        })
        .catch((err) => {
            console.log(err)
        })
}

module.exports = {
    queryDb
}