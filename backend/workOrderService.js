const fs = require("fs");
const { v4: uuidv4 } = require("uuid");

const FILE = "./data/workorders.json";

const createWorkOrder = (craneId, issue) => {

  const data = JSON.parse(fs.readFileSync(FILE));

  const newOrder = {
    id: uuidv4(),
    crane_id: craneId,
    issue,
    priority: "HIGH",
    status: "OPEN",
    created_at: new Date()
  };

  data.push(newOrder);

  fs.writeFileSync(FILE, JSON.stringify(data, null, 2));

  return newOrder;
};

module.exports = { createWorkOrder };