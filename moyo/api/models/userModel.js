const mongoose = require("mongoose");

const userSchema = mongoose.Schema({
  login: { type: String, unique: true },
  email: { type: String, unique: true },
  password: { type: String, unique: true },
  tocken: { type: String },
});

module.exports = mongoose.model("user", userSchema);
