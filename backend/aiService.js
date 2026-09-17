const axios = require("axios");

const getPrediction = async (sensorData) => {
  const res = await axios.post("http://127.0.0.1:8000/predict", sensorData);
  return res.data;
};

module.exports = { getPrediction };