const express = require("express");
const cors = require("cors");
const fs = require("fs");
const csv = require("csv-parser");

const predictRoute = require("./routes/predict");

const app = express();

app.use(cors());
app.use(express.json());

// Existing prediction route
app.use("/api", predictRoute);


// -------------------------------
// GET /api/cranes
// -------------------------------
app.get("/api/cranes", (req, res) => {
  const cranes = [];

  fs.createReadStream("../cranes.csv")
    .pipe(csv())
    .on("data", (row) => cranes.push(row))
    .on("end", () => {
      res.json(cranes);
    })
    .on("error", (err) => {
      console.error("Error reading cranes.csv:", err);
      res.status(500).json({ error: "Failed to read crane data" });
    });
});


// -------------------------------
// GET /api/workorders
// -------------------------------
app.get("/api/workorders", (req, res) => {

  const orders = [];

  fs.createReadStream("../work_orders.csv")
    .pipe(csv())
    .on("data", (row) => orders.push(row))
    .on("end", () => {
      res.json(orders);
    })
    .on("error", (err) => {
      console.error("Error reading work_orders.csv:", err);
      res.status(500).json({ error: "Failed to read work order data" });
    });

});


app.listen(5000, () => {
  console.log("Backend running on port 5000");
});