const mongoose = require("mongoose");

const itemSchema = mongoose.Schema({
  model: { type: String },
  price: { type: String },
  link: { type: String },
  image_url: { type: String },
});

module.exports = mongoose.model("item", itemSchema);
