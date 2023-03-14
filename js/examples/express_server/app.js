const express = require("express");
const otcic = require("otcic");

const PORT = parseInt(process.env.PORT || "8586");
const app = express();

otcic.setup("express_server", "test js cpu");

app.get("/", (req, res) => {
  res.send("Hello World");
});

app.listen(PORT, () => {
  console.log(`Listening for requests on http://localhost:${PORT}`);
});
