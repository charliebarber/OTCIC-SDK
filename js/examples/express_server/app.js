const express = require("express");
const otcic = require("otcic");

const PORT = parseInt(process.env.PORT || "8586");
const app = express();

otcic.setup("express_server");

const d = new Date();
let list = Array(10000).map(x => 10);
app.get("/", (req, res) => {
  let t = d.getUTCSeconds();
  for (let i = 0; i < list.length; i++) {
    for (let j = 0; j < 1000; j++) {
      list[i] = ((list[i] * t * 0.5 + 5) / ((i % 2) + 1)) % 100;
    }
  }
  res.send("Hello World");
});

app.listen(PORT, () => {
  console.log(`Listening for requests on http://localhost:${PORT}`);
});
